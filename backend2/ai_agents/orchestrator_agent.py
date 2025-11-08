import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from ai_agents.hubspot_agent import call_hubspot_agent
from ai_agents.gmail_agent import call_gmail_agent
from ai_agents.slack_agent import call_slack_agent
from ai_agents.calendar_agent import call_calendar_agent

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

@function_tool
async def call_slack_tool(prompt: str) -> str:
    """
    Tool to call the Slack agent.
    
    Args:
        prompt: Text prompt to send to the Slack agent
    
    Returns:
        str: Response from Slack agent
    """
    return await call_slack_agent(prompt)

@function_tool
async def call_calendar_tool(prompt: str) -> str:
    """
    Tool to call the Google Calendar agent.
    
    Args:
        prompt: Text prompt to send to the Calendar agent
    
    Returns:
        str: Response from Calendar agent
    """
    return await call_calendar_agent(prompt)

async def call_orchestrator_agent(prompt: str) -> str:
    """
    Orchestrator agent that routes requests to appropriate agents.
    
    Args:
        prompt: User's request/prompt
    
    Returns:
        str: Response from orchestrator agent
    """
    # Create tools that call the other agents
    tools = [call_hubspot_tool, call_gmail_tool, call_slack_tool, call_calendar_tool]

    agent = Agent(
        name="Orchestrator",
        instructions="""You are an orchestrator agent that routes requests to appropriate agents.
        - Use call_hubspot_tool for CRM-related requests (searching companies, deals, contacts, creating/updating CRM records)
        - Use call_gmail_tool for all email-related requests (drafting emails, sending emails, fetching emails, summarizing emails)
        - Use call_slack_tool for all Slack-related requests (sending Slack messages, fetching conversation history, looking up users, searching messages)
        - Use call_calendar_tool for all calendar-related requests (creating events, modifying events, finding events, listing events, deleting events)
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