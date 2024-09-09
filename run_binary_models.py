#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""


import sentry_sdk
import pandas as pd
from os.path import abspath, join, dirname, isfile
from os import remove, getenv
from datetime import datetime, timedelta
from sqlalchemy import and_
from time import sleep
from json import loads
from asyncio import run
from alpaca.trading.enums import TimeInForce, OrderSide, OrderType
from alpaca.trading.models import Asset
from dotenv import load_dotenv
from uuid import uuid4
from math import ceil

from src.brokerage.alpaca.client import create_trading_client, create_broker_client
from src.brokerage.alpaca.broker import get_clock
from src.brokerage.alpaca.trading import (
    submit_order,
    get_positions,
    close_all_positions,
    close_position,
    get_assets,
)
from src.brokerage.alpaca.utils import get_timestamp_information
from src.brokerage.polygon import create_polygon_client, get_market_data
from src.univariate.analysis import calc_macd
from src.minio import create_minio_client, download_file
from src.sql import (
    create_sql_client,
    get_data,
    insert_data,
    Models,
    PolygonMarketDataDay,
    Transactions,
)
from src.ml.utils import one_hot_encode
from src.utils import log, load_object_from_pickle

load_dotenv()

sentry_sdk.init(
    dsn=getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

if __name__ == "__main__":

    log.error("Preparing to run models.")

    debug_mode = False
    paper = True

    features = [
        "daily_open",  # care should be taken here - daily_open and daily_close are first used to calculate the target variable and then shifted
        "daily_close",
        "daily_macd_histogram",
        # "daily_macd_first_derivative",  # PCA indicates that these are not useful
        # "weekday_monday",
        # "weekday_tuesday",
        # "weekday_wednesday",
        # "weekday_thursday",
        # "weekday_friday",
        "target_date_daily_open",  # this is the open price on the market data for which a prediction is required
    ]

    now = datetime.now()

    path_to_staging = abspath(join(dirname(__file__), "staging"))

    model_offset_hours = 12  # models older than this are not considered valid

    take_profit_percentage: float = 12.0
    stop_loss_percentage: float = 6.0

    alpaca_trading_client = create_trading_client(paper=paper)
    alpaca_broker_client = create_broker_client()
    database_client = create_sql_client()
    minio_client = create_minio_client()
    polygon_client = create_polygon_client()

    timestamp_info = get_timestamp_information(alpaca_broker_client, [now])[0]

    alpaca_clock = get_clock(alpaca_broker_client)
    alpaca_assets: list[Asset] = get_assets(
        alpaca_trading_client, asset_class="us_equity"
    )
    alpaca_assets = [a for a in alpaca_assets if a.tradable]
    shortable_stocks = [e.symbol for e in alpaca_assets if e.shortable]

    market_open_time = alpaca_clock.next_open

    if timestamp_info["open"] is None and not debug_mode:
        log.info("Market does not open today. Exiting process.")
        exit()

    if alpaca_clock.is_open:
        log.info("Market already open. Adjusting market open time.")
        market_open_time -= timedelta(
            days=(now.date() - timestamp_info["previous_trading_date"]).days
        )

    log.info(
        f"Obtaining metadata for models trained since: {now - timedelta(hours=model_offset_hours)}"
    )

    predictive_models = get_data(
        database_client=database_client,
        models=[Models],
        where_clause=and_(
            Models.created_at >= now - timedelta(hours=model_offset_hours),
            Models.precision > 0.6,
            Models.training_set_rows > 200,
            Models.threshold_percentage.is_not(None),
        ),
    )

    log.info("Obtaining model files from object storage.")
    models, models_positive_threshold, models_negative_threshold = {}, {}, {}
    for predictive_model in predictive_models:
        model_location = join(path_to_staging, predictive_model["model_url"])
        if not isfile(model_location):
            download_file(
                minio_client=minio_client,
                bucket_name="models",
                object_name=predictive_model["model_url"],
                file_path=model_location,
            )

        if float(predictive_model["threshold_percentage"]) == 0.0:
            models[loads(predictive_model["symbols"])[0]] = load_object_from_pickle(
                model_location
            )
        elif float(predictive_model["threshold_percentage"]) > 0.0:
            models_positive_threshold[loads(predictive_model["symbols"])[0]] = load_object_from_pickle(
                model_location
            )
        elif float(predictive_model["threshold_percentage"]) < 0.0:
            models_negative_threshold[loads(predictive_model["symbols"])[0]] = load_object_from_pickle(
                model_location
            )

    log.info("Getting historical model inputs.")

    historical_data = get_data(
        database_client=database_client,
        models=[PolygonMarketDataDay],
        where_clause=and_(
            PolygonMarketDataDay.timestamp
            >= (
                timestamp_info["previous_trading_date"] - timedelta(days=40)
            ),  # ensures that sufficient historical data is obtained to calculate trends
            PolygonMarketDataDay.timestamp <= timestamp_info["previous_trading_date"],
            PolygonMarketDataDay.symbol.in_(list(models.keys())),
        ),
    )

    historical_data = pd.DataFrame(historical_data)
    historical_data = historical_data.set_index("timestamp")
    historical_data = historical_data.sort_index()

    prediction_inputs: dict[str, pd.DataFrame] = {}
    for symbol, historical_symbol_data in historical_data.groupby("symbol"):

        _, _, daily_macd_histogram, daily_macd_first_derivative = calc_macd(
            data=historical_symbol_data["close"].to_list(),
        )
        prediction_inputs[symbol] = pd.DataFrame(
            {
                "daily_open": [historical_symbol_data["open"].to_list()[-1]],
                "daily_close": [historical_symbol_data["close"].to_list()[-1]],
                "daily_macd_histogram": [daily_macd_histogram[-1]],
                "daily_macd_first_derivative": [daily_macd_first_derivative[-1]],
                "weekday_monday": [None],
                "weekday_tuesday": [None],
                "weekday_wednesday": [None],
                "weekday_thursday": [None],
                "weekday_friday": [None],
                "target_date_daily_open": [None],
            }
        )

    log.info("Waiting until market open.")

    alpaca_clock = get_clock(alpaca_broker_client)

    if not alpaca_clock.is_open and not debug_mode:
        log.info(
            f"Market does not open until {alpaca_clock.next_open}. Sleeping until then."
        )
        sleep(
            (alpaca_clock.next_open - alpaca_clock.timestamp).seconds + 15 * 60
        )  # Will commence 15 minutes after market open

    log.error("Sleep finished. Commencing strategy.")

    log.info("Getting market open data.")

    market_open_bars = {}
    for symbol in models:
        if open_data := run(
            get_market_data(
                client=polygon_client,
                ticker=symbol,
                from_=market_open_time,
                to=market_open_time,
                timespan="second",
                multiplier=1,
                subtract_day=False,
            )
        ):
            market_open_bars[symbol] = pd.DataFrame(open_data)

    for symbol, target_date_data in market_open_bars.items():
        target_date_data = target_date_data.set_index("timestamp")
        target_date_data = target_date_data.sort_index()
        target_date_data["weekday"] = target_date_data.index.dayofweek
        target_date_data = one_hot_encode(
            target_date_data,
            column="weekday",
            value_mapping={
                0: "monday",
                1: "tuesday",
                2: "wednesday",
                3: "thursday",
                4: "friday",
            },
        )
        prediction_inputs[symbol]["target_date_daily_open"] = target_date_data[
            "open"
        ].to_list()
        prediction_inputs[symbol]["weekday_monday"] = (
            target_date_data["weekday_monday"].to_list()
            if "weekday_monday" in target_date_data.columns
            else [False]
        )
        prediction_inputs[symbol]["weekday_tuesday"] = (
            target_date_data["weekday_tuesday"].to_list()
            if "weekday_tuesday" in target_date_data.columns
            else [False]
        )
        prediction_inputs[symbol]["weekday_wednesday"] = (
            target_date_data["weekday_wednesday"].to_list()
            if "weekday_wednesday" in target_date_data.columns
            else [False]
        )
        prediction_inputs[symbol]["weekday_thursday"] = (
            target_date_data["weekday_thursday"].to_list()
            if "weekday_thursday" in target_date_data.columns
            else [False]
        )
        prediction_inputs[symbol]["weekday_friday"] = (
            target_date_data["weekday_friday"].to_list()
            if "weekday_friday" in target_date_data.columns
            else [False]
        )

    log.info("Running models.")

    predictions = {
        symbol: int(models[symbol].predict(prediction_inputs[symbol][features])[0])
        for symbol in market_open_bars
    }
    predictions_positive_threshold = {
        symbol: int(models_positive_threshold[symbol].predict(prediction_inputs[symbol][features])[0])
        for symbol in market_open_bars
    }
    predictions_negative_threshold = {
        symbol: int(models_negative_threshold[symbol].predict(prediction_inputs[symbol][features])[0])
        for symbol in market_open_bars
    }

    log.info("Taking positions.")


    long_positions, short_positions = 0, 0
    for symbol, prediction in predictions.items():
        if prediction and models_positive_threshold[symbol]:
            long_positions += 1
        if not prediction and models_negative_threshold[symbol]:
            short_positions += 1

    long_open_prices, short_open_prices = [], []
    for symbol, prediction in predictions.items():
        if prediction and models_positive_threshold[symbol]:
            long_open_prices.append(float(market_open_bars[symbol]["open"][0]))
        if not prediction and models_negative_threshold[symbol] and symbol in shortable_stocks:
            short_open_prices.append(float(market_open_bars[symbol]["open"][0]))

    estimated_total_position = sum(long_open_prices) - sum(short_open_prices)

    log.info(
        f"Estimated total long: {sum(long_open_prices)} (min: {min(long_open_prices)}, max: {max(long_open_prices)})"
    )
    log.info(
        f"Estimated total short: {sum(short_open_prices)} (min: {min(short_open_prices)}, max: {max(short_open_prices)})"
    )
    log.info(f"Estimated total position: {estimated_total_position}")

    potential_total_transactions = len(long_open_prices) + len(short_open_prices)
    cash = float(alpaca_trading_client.get_account().cash)

    for symbol, prediction in predictions.items():
        if (prediction and models_positive_threshold[symbol]) or (not prediction and models_negative_threshold[symbol]):
            log.info(f"Preparing to trade symbol: {symbol}")
            if symbol in [e.symbol for e in alpaca_assets]:
                log.info("Stock can be traded.")
                if not prediction and symbol not in shortable_stocks:
                    log.info("Symbol cannot be shorted.")
                    continue

                limit_price = prediction_inputs[symbol]["target_date_daily_open"].to_list()[
                    0
                ]

                submit_order(
                    client=alpaca_trading_client,
                    symbol=symbol,
                    quantity=2 * ceil(cash / limit_price / potential_total_transactions),
                    side=OrderSide.BUY if prediction else OrderSide.SELL,
                    order_type=OrderType.LIMIT,
                    time_in_force=TimeInForce.DAY,
                    limit_price=limit_price,
                    stop_price=None,
                    trail_percent=None,
                )

    log.info("Monitoring performance.")

    alpaca_clock = get_clock(alpaca_broker_client)

    while alpaca_clock.timestamp < alpaca_clock.next_close - timedelta(seconds=90):

        positions = get_positions(
            client=alpaca_trading_client,
        )

        for position in positions:
            close_this_position = False
            gone_short = str(position.side) == "PositionSide.SHORT"
            log.info(f"Checking position {position.side} for symbol: {position.symbol}")
            movement_percentage = (
                100
                * (float(position.market_value) - float(position.cost_basis))
                / float(position.cost_basis)
            )
            if (movement_percentage >= take_profit_percentage and not gone_short) or (
                -movement_percentage >= take_profit_percentage and gone_short
            ):
                log.info(f"Taking profit of: {round(abs(movement_percentage), 2)}%")
                close_this_position = True
            if (movement_percentage >= stop_loss_percentage and gone_short) or (
                -movement_percentage >= stop_loss_percentage and not gone_short
            ):
                log.info(f"Realizing loss of: {round(abs(movement_percentage), 2)}%")
                close_this_position = True

            if close_this_position:
                log.error(
                    f"Closing position on symbol: {symbol} with change: {round(abs(movement_percentage), 2)}%"
                )
                close_position(
                    client=alpaca_trading_client,
                    symbol=position.symbol,
                )

                model_id: str | None = None
                if model_metadata := [
                    e
                    for e in predictive_models
                    if position.symbol in e["symbols"]
                ]:
                    model_id = model_metadata[0]["model_id"]

                insert_data(
                    database_client=database_client,
                    documents=[
                        Transactions(
                            transaction_id=str(uuid4()),
                            description=f"Limit: for {round(position.qty, 2)} shares at {round(movement_percentage, 2)} in {position.symbol}",
                            ticker=position.symbol,
                            placed_timestamp=alpaca_clock.timestamp.date(),
                            accepted_timestamp=alpaca_clock.timestamp,
                            order_type="Limit",
                            side=(
                                "short"
                                if str(position.side) == "PositionSide.SHORT"
                                else "long"
                            ),
                            entry_price=position.cost_basis,
                            exit_price=position.market_value,
                            currency="USD",
                            quantity=position.qty,
                            exchange=position.exchange,
                            broker="Alpaca",
                            paper=paper,
                            backtest=False,
                            live=not paper,
                            created_at=alpaca_clock.timestamp,
                            last_modified_at=alpaca_clock.timestamp,
                            model_id=model_id,
                        )
                    ],
                )

        sleep(60)
        alpaca_clock = get_clock(alpaca_broker_client)
        log.info(f"Current market time: {alpaca_clock.timestamp}")

    log.info("Reached end of trading. Closing positions.")

    positions = get_positions(
        client=alpaca_trading_client,
    )

    for position in positions:
        close_position(
            client=alpaca_trading_client,
            symbol=position.symbol,
        )
        model_id: str | None = None
        if model_metadata := [
            e for e in predictive_models if position.symbol in e["symbols"]
        ]:
            model_id = model_metadata[0]["model_id"]
        insert_data(
            database_client=database_client,
            documents=[
                Transactions(
                    transaction_id=str(uuid4()),
                    description=f"Limit: for {round(position.qty, 2)} shares at {round(movement_percentage, 2)} in {position.symbol}",
                    ticker=position.symbol,
                    placed_timestamp=alpaca_clock.timestamp.date(),
                    accepted_timestamp=alpaca_clock.timestamp,
                    order_type="Limit",
                    side=(
                        "short"
                        if str(position.side) == "PositionSide.SHORT"
                        else "long"
                    ),
                    entry_price=position.cost_basis,
                    exit_price=position.market_value,
                    currency="USD",
                    quantity=position.qty,
                    exchange=position.exchange,
                    broker="Alpaca",
                    paper=paper,
                    backtest=False,
                    live=not paper,
                    created_at=alpaca_clock.timestamp,
                    last_modified_at=alpaca_clock.timestamp,
                    model_id=model_id,
                )
            ],
        )

    close_all_positions(
        client=alpaca_trading_client,
        cancel_orders=True,
    )

    log.info("Recording outcomes.")

    log.info("Tidying up.")

    for predictive_model in predictive_models:
        if isfile(join(path_to_staging, predictive_model["model_url"])):
            remove(join(path_to_staging, predictive_model["model_url"]))

    log.error("Completed running models.")
