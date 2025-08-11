import os
import boto3
from botocore.exceptions import ClientError, ParamValidationError
from strands import tool
from constants import BUCKET_NAME, AWS_REGION

@tool(description="Upload a local file to an AWS S3 bucket. Takes a file path and optional bucket name, returns the uploaded S3 object key.")
def upload_to_s3(file_path: str, bucket_name: str = BUCKET_NAME) -> str:
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
    return object_key