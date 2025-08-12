import os
import boto3
from botocore.exceptions import ClientError, ParamValidationError
from strands import tool
from constants import BUCKET_NAME, AWS_REGION

@tool(description="Upload a local file to an AWS S3 bucket. Takes a file path and optional bucket name, returns a success message with the S3 URI.")
def upload_to_s3(file_path: str, bucket_name: str = BUCKET_NAME) -> str:
    """
    Upload a local file to an AWS S3 bucket.

    Use this tool when you need to persist a local file to Amazon S3 for later
    retrieval, sharing, or downstream processing. Provide the absolute or
    relative path to a file on disk. The S3 object key is derived from the
    file's base name; if an object with the same key already exists in the
    target bucket, it will be overwritten.

    This tool authenticates using your environment's AWS credentials and
    uploads to the configured AWS region. The transfer uses boto3's managed
    uploader, which supports multipart uploads for large files.

    Example response:
        "Uploaded to s3://my-bucket/audio.wav"

    Notes:
        - The S3 object key is `os.path.basename(file_path)`; prefixes/folders
          are not supported by this tool
        - The destination bucket must already exist and you must have
          `s3:PutObject` permission on it
        - Existing objects with the same key will be overwritten
        - Server-side encryption, ACLs, metadata, and storage class are not set
          by default
        - Status messages are printed to stdout; on success, this function
          returns a success message including the S3 URI; on errors, it returns
          an error string prefixed with "ERROR:"
        - AWS region comes from `constants.AWS_REGION`; the default bucket comes
          from `constants.BUCKET_NAME`

    Args:
        file_path: Path to the local file to upload. Example:
                   "./outputs/audio.wav" or "/tmp/report.pdf"
        bucket_name: Destination S3 bucket name (default: `constants.BUCKET_NAME`)

    Returns:
        On success: A success message (string) containing the S3 URI, e.g.,
                    "Uploaded to s3://bucket-name/audio.wav"
        On failure: An error message (string) starting with "ERROR: ..."
    """
    print(f"Uploading file {file_path} to bucket {bucket_name} (region: {AWS_REGION})")

    s3_client = boto3.client("s3", region_name=AWS_REGION)
    object_key = os.path.basename(file_path)

    try:
        s3_client.upload_file(Filename=file_path, Bucket=bucket_name, Key=object_key)
    except FileNotFoundError:
        error_message = f"ERROR: File not found: {file_path}"
        print(error_message)
        return error_message
    except (ParamValidationError, ClientError) as error:
        error_message = f"ERROR: Failed to upload {file_path} to s3://{bucket_name}/{object_key}: {error}"
        print(error_message)
        return error_message

    success_message = f"Uploaded to s3://{bucket_name}/{object_key}"
    print(success_message)
    return success_message