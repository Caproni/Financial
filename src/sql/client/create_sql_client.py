#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from os import getenv
from dotenv import load_dotenv

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from src.utils import log

Base = declarative_base()


class DatabaseClient:
    def __init__(
        self,
        engine,
        SessionLocal,
        log_queries: bool = False,
    ):
        self.engine = engine
        self.SessionLocal = SessionLocal
        self.log_queries = log_queries

        if self.log_queries:
            self._setup_query_logging()

    def _setup_query_logging(self):
        """
        Sets up query logging if the log_queries flag is True.
        """

        @event.listens_for(self.engine, "before_cursor_execute")
        def before_cursor_execute(
            conn, cursor, statement, parameters, context, executemany
        ):
            log.info(f"Executing query: {statement}")
            log.info(f"With parameters: {parameters}")

    @contextmanager
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


def create_sql_client(log_queries: bool = False) -> DatabaseClient:
    """
    Creates a DatabaseClient instance.

    Args:
        log_queries: bool - Whether to log SQL queries as they are executed.

    Returns:
        DatabaseClient - The configured DatabaseClient instance.
    """
    log.function_call()

    load_dotenv()

    host = getenv("POSTGRES_HOST")
    port = getenv("POSTGRES_PORT")
    database = getenv("POSTGRES_DATABASE")
    username = getenv("POSTGRES_USERNAME")
    password = getenv("POSTGRES_PASSWORD")

    database_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"

    engine = create_engine(database_url, echo=log_queries)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return DatabaseClient(
        engine=engine, SessionLocal=SessionLocal, log_queries=log_queries
    )
