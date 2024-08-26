#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from minio import Minio
from dotenv import load_dotenv
from os import getenv

from src.utils import log


def create_minio_client():
    """
    Creates and returns a MinIO client instance configured with environment variables.

    This function initializes a MinIO client using the host, port, access key, and secret key retrieved from environment variables. It logs the function call and ensures that the necessary environment variables are loaded before creating the client.

    Returns:
        Minio: An instance of the MinIO client configured with the specified credentials.

    Examples:
        client = create_minio_client()
    """
    log.function_call()

    load_dotenv()

    return Minio(
        f"{getenv("MINIO_HOST")}:{getenv("MINIO_PORT")}",
        access_key=getenv("MINIO_ACCESS_KEY"),
        secret_key=getenv("MINIO_SECRET_KEY"),
        secure=False,
    )
