from strands import Agent
from strands.models.bedrock import BedrockModel
from transcribe_tool import transcribe
from yt_dl_tool import download_youtube_audio
from upload_to_s3_tool import upload_to_s3
from strands_tools import use_aws
import logging

# Enables Strands debug log level
# logging.getLogger("strands").setLevel(logging.DEBUG)

# Sets the logging format and streams logs to stderr
# logging.basicConfig(
#     format="%(levelname)s | %(name)s | %(message)s",
#     handlers=[logging.StreamHandler()]
# )

model = BedrockModel(
    region_name="eu-north-1",
    model_id="eu.anthropic.claude-sonnet-4-20250514-v1:0"
)

coordinator_agent = Agent(
    name="Coordinator Agent",
    description="A agent that can generate AWS certification-like questions from a YouTube video",
    tools=[download_youtube_audio, upload_to_s3, transcribe, use_aws],
    model=model,
)

coordinator_agent(
"""
    Download the audio from this video: https://www.youtube.com/watch?v=W1zGjrH3BJI&ab_channel=TinyTechnicalTutorials, 
    upload it to S3,
    transcribe it to text, 
    and then create a set of 5 questions aws certification-like questions based on the transcribed text
""")