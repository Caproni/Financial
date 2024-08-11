#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import Column, Boolean, String, UUID
from ..client import Base


class TickerNews(Base):
    """Example:

    {
    "results": [
        {
            "id": "4fd9f3a653f3d1c6d99a21d7cc62b883e8547109c95778e34de7c6c9ecaccfe4",
            "publisher": {
                "name": "The Motley Fool",
                "homepage_url": "https://www.fool.com/",
                "logo_url": "https://s3.polygon.io/public/assets/news/logos/themotleyfool.svg",
                "favicon_url": "https://s3.polygon.io/public/assets/news/favicons/themotleyfool.ico"
            },
            "title": "Warren Buffett Is Slashing Berkshire Hathaway's Position in Apple Stock",
            "author": "Parkev Tatevosian, Cfa",
            "published_utc": "2024-08-08T14:16:30Z",
            "article_url": "https://www.fool.com/investing/2024/08/08/warren-buffett-is-slashing-berkshire-hathaways-pos/?source=iedfolrf0000001",
            "tickers": [
                "AAPL"
            ],
            "image_url": "https://g.foolcdn.com/editorial/images/786449/buffett17-tmf.jpg",
            "description": "Warren Buffett, the renowned investor, has sold a significant portion of his Apple stock holdings, worth around $90 billion. This move has raised questions about whether it could be Buffett's biggest investing mistake.",
            "keywords": [
                "Warren Buffett",
                "Apple",
                "investing"
            ],
            "insights": [
                {
                    "ticker": "AAPL",
                    "sentiment": "negative",
                    "sentiment_reasoning": "The article suggests that Buffett's decision to sell a large portion of his Apple stock holdings could be a mistake, implying a negative sentiment towards the company's future performance."
                }
            ]
        },
        {
            "id": "931602cbcfeb06e22188e205a1cb6127215b7a62e9a37e5cc7a935e8376ac402",
            "publisher": {
                "name": "The Motley Fool",
                "homepage_url": "https://www.fool.com/",
                "logo_url": "https://s3.polygon.io/public/assets/news/logos/themotleyfool.svg",
                "favicon_url": "https://s3.polygon.io/public/assets/news/favicons/themotleyfool.ico"
            },
            "title": "Prediction: 1 Unstoppable Stock Will Join Nvidia, Apple, Microsoft, and Alphabet in the $2 Trillion Club Within 3 Years",
            "author": "The Motley Fool",
            "published_utc": "2024-08-08T10:40:00Z",
            "article_url": "https://www.fool.com/investing/2024/08/08/prediction-1-stock-nvidia-microsoft-in-2-trillion/?source=iedfolrf0000001",
            "tickers": [
                "META",
                "NVDA",
                "AAPL",
                "MSFT",
                "GOOG",
                "GOOGL"
            ],
            "image_url": "https://g.foolcdn.com/editorial/images/785914/two-people-laughing-while-watching-a-video-on-a-smartphone.jpg",
            "description": "Meta Platforms (META) is predicted to join the $2 trillion club within 3 years, driven by its advancements in artificial intelligence and potential to drive significant returns for investors.",
            "keywords": [
                "Meta Platforms",
                "Artificial Intelligence",
                "Stock Prediction"
            ],
            "insights": [
                {
                    "ticker": "META",
                    "sentiment": "positive",
                    "sentiment_reasoning": "The article predicts that Meta Platforms will join the $2 trillion club within 3 years, driven by its advancements in artificial intelligence and potential to drive significant returns for investors."
                },
                {
                    "ticker": "NVDA",
                    "sentiment": "positive",
                    "sentiment_reasoning": "Nvidia is mentioned as one of the companies currently valued at over $2 trillion, indicating its strong market position."
                },
                {
                    "ticker": "AAPL",
                    "sentiment": "positive",
                    "sentiment_reasoning": "Apple is mentioned as one of the companies currently valued at over $2 trillion, indicating its strong market position."
                },
                {
                    "ticker": "MSFT",
                    "sentiment": "positive",
                    "sentiment_reasoning": "Microsoft is mentioned as one of the companies currently valued at over $2 trillion, indicating its strong market position."
                },
                {
                    "ticker": "GOOG",
                    "sentiment": "positive",
                    "sentiment_reasoning": "Alphabet is mentioned as one of the companies currently valued at over $2 trillion, indicating its strong market position."
                },
                {
                    "ticker": "GOOGL",
                    "sentiment": "positive",
                    "sentiment_reasoning": "Alphabet is mentioned as one of the companies currently valued at
    """

    __tablename__ = "ticker_news"

    ticker = Column(String, nullable=False)
    name = Column(String, primary_key=True, nullable=True)
    market = Column(String, nullable=False)
    locale = Column(String, nullable=False)
    primary_exchange = Column(String, nullable=True)
    type = Column(String, nullable=True)
    active = Column(Boolean, nullable=False)
    currency_name = Column(String, nullable=True)
    cik = Column(String, nullable=True)
    composite_figi = Column(String, nullable=True)
    share_class_figi = Column(String, nullable=True)
    last_updated_utc = Column(String, nullable=True)
    ticker_news_id = Column(UUID, nullable=False)
