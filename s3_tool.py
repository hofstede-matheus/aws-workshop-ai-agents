from strands import Agent
from strands import tool
from strands_tools import use_aws
from constants import BUCKET_NAME

@tool(description="Upload a file to an AWS S3 bucket. Takes a file path and optional bucket name, returns the response from the upload operation.")
def upload_to_s3(file_path: str, bucket_name: str = BUCKET_NAME) -> str:
  # Create agent with AWS capabilities
  agent = Agent(tools=[use_aws])

  # Use the agent to upload files
  response = agent(f"Upload the file {file_path} to my S3 bucket called {bucket_name}")
  return response