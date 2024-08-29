#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from os.path import abspath, join, dirname
from minio import Minio
from src.minio import create_minio_client, upload_file


def test_create_minio_client():

    minio_client = create_minio_client()

    assert isinstance(minio_client, Minio)


def test_upload_file():

    minio_client = create_minio_client()
    test_file = abspath(join(dirname(__file__), "assets/txt", "example.txt"))

    upload_file(
        minio_client=minio_client,
        bucket_name="test",
        object_name="example.txt",
        file_path=test_file,
    )
