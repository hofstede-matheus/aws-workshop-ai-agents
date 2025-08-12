import time
import boto3
from strands import tool
from constants import AWS_ROLE_ARN, BUCKET_NAME, AWS_REGION

@tool(description="Transcribe an audio file stored in an AWS S3 bucket to text and save it to a text file in the same bucket.")
def transcribe(audio_file: str, bucket_name: str = BUCKET_NAME) -> str:
    """
    Transcribe an audio file in S3 to text and save the transcript back to S3.

    Use this tool when you need to convert spoken audio to text using Amazon
    Transcribe. Provide the S3 object key (not a full URI) of the audio file in
    the target bucket. The transcript is written to the same bucket as a text
    file named `transcription-{audio_file}.txt`.

    The job runs synchronously here (this function polls until completion) and
    uses the configured AWS region. The language is set to "en-US" and the media
    format is forced to MP3.

    Example response:
        "Transcription job transcription-audio.mp3-1700000000 finished with status: COMPLETED, save to s3://my-bucket/transcription-audio.mp3.txt"

    Notes:
        - The input must be an MP3 file; the media format is hard-coded to "mp3"
        - The destination bucket must exist in `constants.AWS_REGION`
        - You must have permissions for Transcribe and S3, and `constants.AWS_ROLE_ARN`
          must grant data access (used with deferred execution)
        - Large files may take several minutes; the function polls every 5 seconds
        - Only the default language "en-US" is supported in this tool
        - Status messages are printed to stdout; the function returns a summary
          string containing the job status and transcript S3 URI

    Args:
        audio_file: S3 object key of the audio file to transcribe (e.g., "audio.mp3").
                    Do not include the bucket name or the `s3://` prefix.
        bucket_name: Name of the S3 bucket that contains the audio and where the
                     transcript will be saved (default: `constants.BUCKET_NAME`).

    Returns:
        A status message (string) including the Transcribe job name, final
        status (e.g., COMPLETED or FAILED), and the transcript S3 URI.
    """
    print(f"Transcribing file {audio_file} located in bucket {bucket_name} from region {AWS_REGION} ...")

    # Create Transcribe client
    transcribe_client = boto3.client("transcribe", region_name=AWS_REGION)

    # Derive a simple, valid job name from the file name and timestamp
    job_name = f'transcription-{audio_file}-{int(time.time())}'

    output_key = f"transcription-{audio_file}.txt"

    print(f"Starting Transcribe job: {job_name}")
    start_params = {
        "TranscriptionJobName": job_name,
        "Media": {"MediaFileUri": f"s3://{bucket_name}/{audio_file}"},
        "MediaFormat": "mp3",
        "LanguageCode": "en-US",
        "OutputBucketName": bucket_name,
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
        job_status = response["TranscriptionJob"]["TranscriptionJobStatus"]
        print(f"Transcription job status: {job_status}")

        if job_status in ["COMPLETED", "FAILED"]:
            break

        time.sleep(5)

    return f"Transcription job {job_name} finished with status: {job_status}, save to {output_uri}"


