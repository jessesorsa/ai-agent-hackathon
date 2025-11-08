import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from ai_agents.hubspot_agent import call_hubspot_agent
from ai_agents.gmail_agent import call_gmail_agent

# Load environment variables
load_dotenv()

@function_tool
async def call_hubspot_tool(prompt: str) -> str:
    """
    Tool to call the HubSpot agent.
    
    Args:
        prompt: Text prompt to send to the HubSpot agent
    
    Returns:
        str: Response from HubSpot agent
    """
    return await call_hubspot_agent(prompt)

@function_tool
async def call_gmail_tool(prompt: str) -> str:
    """
    Tool to call the Gmail agent.
    
    Args:
        prompt: Text prompt to send to the Gmail agent
    
    Returns:
        str: Response from Gmail agent
    """
    return await call_gmail_agent(prompt)

async def call_orchestrator_agent(prompt: str) -> str:
    """
    Orchestrator agent that routes requests to appropriate agents.
    
    Args:
        prompt: User's request/prompt
    
    Returns:
        str: Response from orchestrator agent
    """
    # Create tools that call the other agents
    tools = [call_hubspot_tool, call_gmail_tool]

    agent = Agent(
        name="Orchestrator",
        instructions="""You are an orchestrator agent that routes requests to appropriate agents.
        - Use call_hubspot_tool for CRM-related requests (searching companies, deals, contacts, creating/updating CRM records)
        - Use call_gmail_tool for email-related requests (drafting emails, sending emails, fetching emails)
        - You can use multiple tools if needed to fulfill a request.""",
        tools=tools,
        model="gpt-4.1-mini"
    )

    result = await Runner.run(
        starting_agent=agent,
        input=prompt,
    )
    
    print(result.final_output)
    return result.final_output