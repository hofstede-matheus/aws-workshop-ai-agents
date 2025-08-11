import time
import boto3
from botocore.exceptions import ClientError, ParamValidationError
from strands import tool
from constants import AWS_ROLE_ARN, BUCKET_NAME, AWS_REGION

@tool(description="Transcribe an audio file stored in an AWS S3 bucket to text and save it to a text file in the same bucket.")
def transcribe(audio_file: str, bucket_name: str = BUCKET_NAME) -> str:
    print("Transcribing file...")
    print(f"File: {audio_file}")
    print(f"Bucket: {bucket_name}")
    print(f"Region: {AWS_REGION}")

    # Create Transcribe client
    transcribe_client = boto3.client("transcribe", region_name=AWS_REGION)

    # Derive a simple, valid job name from the file name and timestamp
    job_name = f'transcription-{audio_file}-{int(time.time())}'

    # Always use mp3 as media format
    media_format = "mp3"
    output_key = f"transcricao-{audio_file}.txt"

    print(f"Starting Transcribe job: {job_name}")
    start_params = {
        "TranscriptionJobName": job_name,
        "Media": {"MediaFileUri": f"s3://{bucket_name}/{audio_file}"},
        "MediaFormat": media_format,
        "LanguageCode": "en-US",
        "OutputBucketName": bucket_name,
        # If supported in your account/region, OutputKey lets you control S3 object key/prefix
        "OutputKey": output_key,
        "JobExecutionSettings": {
            "AllowDeferredExecution": True,
            "DataAccessRoleArn": AWS_ROLE_ARN,
        },
    }

    transcribe_client.start_transcription_job(**start_params)

    output_uri = f"s3://{bucket_name}/{output_key}"

    # Poll for job completion
    while True:
        response = transcribe_client.get_transcription_job(
            TranscriptionJobName=job_name
        )
        print(response)
        job_status = response["TranscriptionJob"]["TranscriptionJobStatus"]
        print(f"Transcription job status: {job_status}")

        if job_status in ["COMPLETED", "FAILED"]:
            break

        time.sleep(5)

    return f"Transcription job {job_name} finished with status: {job_status}, save to {output_uri}"


