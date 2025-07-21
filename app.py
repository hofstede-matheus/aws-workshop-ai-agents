from strands import Agent
from strands.models.bedrock import BedrockModel
from yt_dl_tool import download_youtube_audio
from s3_tool import upload_to_s3
from constants import BUCKET_NAME

print("Hello World")


model = BedrockModel(
    region_name="eu-north-1",
    model_id="eu.anthropic.claude-sonnet-4-20250514-v1:0"
)

coordinator_agent = Agent(
    name="Coordinator Agent",
    description="A agent that can generate AWS certification-like questions from a YouTube video",
    tools=[download_youtube_audio, upload_to_s3],
    model=model,
)

coordinator_agent("Download the audio from this video: https://www.youtube.com/watch?v=W1zGjrH3BJI&ab_channel=TinyTechnicalTutorials and then upload it to S3")