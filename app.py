from strands import Agent
from strands.models.bedrock import BedrockModel
from strands_tools import calculator

print("Hello World")

model = BedrockModel(
    region_name="eu-north-1",
    model_id="eu.anthropic.claude-sonnet-4-20250514-v1:0"
)

agent = Agent(
    name="Calculator",
    description="A calculator agent that can perform basic arithmetic operations",
    tools=[calculator],
    model=model,
)

agent("What is 10 + 10?")
