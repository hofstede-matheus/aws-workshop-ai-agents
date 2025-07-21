from strands import Agent
from strands.models.bedrock import BedrockModel
from yt_dl_tool import download_youtube_audio
print("Hello World")

model = BedrockModel(
    region_name="eu-north-1",
    model_id="eu.anthropic.claude-sonnet-4-20250514-v1:0"
)

agent = Agent(
    name="Calculator",
    description="A calculator agent that can perform basic arithmetic operations",
    tools=[download_youtube_audio],
    model=model,
)

agent("Download the audio from this video: https://www.youtube.com/watch?v=W1zGjrH3BJI&ab_channel=TinyTechnicalTutorials")