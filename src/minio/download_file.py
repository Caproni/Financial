#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from minio import Minio
from minio.error import S3Error

from src.utils import log


def download_file(
    minio_client: Minio,
    bucket_name: str,
    object_name: str,
    file_path: str,
):
    """
    Downloads a file from a specified MinIO bucket to a local file path.

    This function retrieves a file from a MinIO bucket using the provided bucket name and object name, saving it to the specified file path. It logs the success of the operation or any errors that occur during the download process.

    Args:
        minio_client (Minio): A Minio client.
        bucket_name (str): The name of the bucket from which to download the file.
        object_name (str): The name of the object to download.
        file_path (str): The local path where the downloaded file will be saved.

    Returns:
        None

    Raises:
        S3Error: If there is an error during the file download process.

    Examples:
        download_file('my-bucket', 'my-object.txt', '/local/path/my-object.txt')
    """

    log.function_call()
    try:
        minio_client.fget_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=file_path,
        )
        log.info(
            f"File '{object_name}' downloaded successfully from bucket '{bucket_name}' to '{file_path}'."
        )

    except S3Error as err:
        log.error(f"Error occurred: {err}")
