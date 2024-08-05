#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from os import getenv
from dotenv import load_dotenv

from sqlalchemy import create_engine
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
    ):
        self.engine = engine
        self.SessionLocal = SessionLocal

    @contextmanager
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


def create_sql_client() -> DatabaseClient:

    log.function_call()

    load_dotenv()

    host = getenv("POSTGRES_HOST")
    port = getenv("POSTGRES_PORT")
    database = getenv("POSTGRES_DATABASE")
    username = getenv("POSTGRES_USERNAME")
    password = getenv("POSTGRES_PASSWORD")

    database_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return DatabaseClient(engine=engine, SessionLocal=SessionLocal)
