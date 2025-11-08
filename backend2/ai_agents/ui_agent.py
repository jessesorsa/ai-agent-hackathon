import os
from openai import OpenAI

from dotenv import load_dotenv

from composio import Composio
from agents import Agent, Runner
from composio_openai_agents import OpenAIAgentsProvider

# Load environment variables
load_dotenv()

# Initialize the client with your C1 API Key and the C1 Base URL
client = OpenAI(
    api_key=os.environ.get("THESYS_API_KEY"),
    base_url="https://api.thesys.dev/v1/embed"
)

async def call_ui_agent(prompt: str) -> str:
    """
    Call UI agent to create UI.
    
    Args:
        prompt: request/prompt
    
    Returns:
        str: UI component
    """
    
    print(prompt)
    
    completion = client.chat.completions.create(
        model="c1/anthropic/claude-sonnet-4/v-20250930",
        messages=[
            {"role": "system", "content": "You generate UI widgets for sales workflows."},
            {"role": "user", "content": prompt}
        ],
    )
    assistant_response = completion.choices[0].message
    return {"ui": assistant_response.content}