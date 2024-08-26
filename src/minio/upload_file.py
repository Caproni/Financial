#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from minio import Minio
from minio.error import S3Error

from src.utils import log


def upload_file(
    minio_client: Minio,
    bucket_name: str,
    object_name: str,
    file_path: str,
):
    """
    Uploads a file to a specified MinIO bucket, creating the bucket if it does not exist.

    This function checks whether the specified bucket exists and creates it if necessary before uploading the file to the bucket. It logs the success of the upload or any errors that may occur during the process.

    Args:
        minio_client (Minio): The MinIO client used to interact with the MinIO server.
        bucket_name (str): The name of the bucket to which the file will be uploaded.
        object_name (str): The name under which the file will be stored in the bucket.
        file_path (str): The local path of the file to be uploaded.

    Returns:
        None

    Raises:
        S3Error: If there is an error during the file upload process.

    Examples:
        upload_file(client, 'my-bucket', 'my-object.txt', '/local/path/my-object.txt')
    """

    log.function_call()
    try:
        if not minio_client.bucket_exists(bucket_name):
            log.info(f"Bucket '{bucket_name}' does not exist. Creating it.")
            minio_client.make_bucket(bucket_name)

        minio_client.fput_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=file_path,
        )
        log.info(
            f"File '{file_path}' uploaded successfully to bucket '{bucket_name}' as '{object_name}'."
        )

    except S3Error as err:
        log.error(f"Error occurred: {err}")
