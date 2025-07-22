from strands import Agent
from strands import tool
from strands_tools import use_aws
from constants import BUCKET_NAME, AWS_REGION
import base64

@tool(description="Upload a file to an AWS S3 bucket. Takes a file path and optional bucket name, returns the response from the upload operation.")
def upload_to_s3(file_path: str, bucket_name: str = BUCKET_NAME) -> str:
  # Create agent with AWS capabilities
  agent = Agent(tools=[use_aws])

  print(f"Uploading file {file_path} to bucket {bucket_name}")

  # Read the file content as bytes and encode as base64
  with open(file_path, "rb") as f:
      file_content = f.read()
      file_content_b64 = base64.b64encode(file_content).decode('utf-8')


  result = agent.tool.use_aws(
      service_name="s3", 
      operation_name="put_object",
      parameters={
          "Bucket": bucket_name,
          "Key": file_path.split("/")[-1],
          "Body": file_content_b64
      },
      region=AWS_REGION,
      label=f"Upload file {file_path} to bucket {bucket_name}"
  )

  print(result)
  return result
  # Use the agent to upload files
  # response = agent(f"Upload the file audio.mp3 to my S3 bucket called {bucket_name}")
  # return response