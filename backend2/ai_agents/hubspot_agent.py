import os
from dotenv import load_dotenv
import os

from composio import Composio
from agents import Agent, Runner
from composio_openai_agents import OpenAIAgentsProvider

# Load environment variables
load_dotenv()

composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"), provider=OpenAIAgentsProvider())

 
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
    tools = composio.tools.get(user_id=externalUserId, 
        tools=["HUBSPOT_SEARCH_COMPANIES", "HUBSPOT_SEARCH_DEALS", "HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA", 
               "HUBSPOT_GET_COMPANY", "HUBSPOT_CREATE_COMPANY", 
               "HUBSPOT_CREATE_DEAL", "HUBSPOT_CREATE_CONTACT", "HUBSPOT_UPDATE_DEAL"])

    agent = Agent(
        name="Hubspot Manager", 
        instructions="You are a helpful assistant", 
        tools=tools,
        model="gpt-4.1-mini"
    )

    result = await Runner.run(
        starting_agent=agent,
        input=prompt,
    )
    
    print(result.final_output)
    return result.final_output