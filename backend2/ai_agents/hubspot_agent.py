from dotenv import load_dotenv

from composio import Composio
from agents import Agent, Runner
from composio_openai_agents import OpenAIAgentsProvider

# Load environment variables
load_dotenv()

composio = Composio(api_key="ak_GejSN5EyYHRkudj6yqaI", provider=OpenAIAgentsProvider())

 
async def call_hubspot_agent(prompt: str) -> str:
    """
    Call HubSpot agent to process CRM-related requests.
    
    Args:
        prompt: User's request/prompt
    
    Returns:
        str: Response from HubSpot agent
    """
    # Get Gmail tools that are pre-configured
    externalUserId = "pg-test-5ebc0c28-44d2-4653-a6eb-5dc8942828e9"
    tools = composio.tools.get(user_id=externalUserId, tools=["HUBSPOT_SEARCH_COMPANIES", "HUBSPOT_GET_COMPANY"])

    agent = Agent(
        name="Hubspot Manager", instructions="You are a helpful assistant", tools=tools
    )

    result = await Runner.run(
        starting_agent=agent,
        input=prompt,
    )
    
    print(result.final_output)
    return result.final_output