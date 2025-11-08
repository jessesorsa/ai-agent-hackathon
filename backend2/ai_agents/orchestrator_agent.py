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
    Call the HubSpot CRM agent to handle CRM-related operations.
    
    Use this tool for:
    - Searching for companies, deals, or contacts in HubSpot
    - Creating new companies, deals, or contacts
    - Updating existing CRM records (deals, contacts, companies)
    - Retrieving information about specific CRM entities
    
    Args:
        prompt: A natural language request describing the CRM operation you want to perform.
               Examples: "Search for companies named Acme", "Create a new deal for $50k",
               "Find contacts in the tech industry", "Update deal status to closed-won"
    
    Returns:
        str: The response from the HubSpot agent containing the results of the CRM operation
    """
    return await call_hubspot_agent(prompt)

@function_tool
async def call_gmail_tool(prompt: str) -> str:
    """
    Call the Gmail agent to handle email-related operations.
    
    Use this tool for:
    - Drafting new emails based on user requests
    - Sending emails to recipients
    - Fetching/searching for emails in Gmail
    - Managing email drafts
    
    Args:
        prompt: A natural language request describing the email operation you want to perform.
               Examples: "Draft an email to john@example.com about the meeting",
               "Send a follow-up email to the client", "Find emails from last week"
    
    Returns:
        str: The response from the Gmail agent containing the email draft, confirmation, or search results
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
    s
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
        model="gpt-4o-mini"
    )

    result = await Runner.run(
        starting_agent=agent,
        input=prompt,
    )
    
    print(result.final_output)
    return result.final_output