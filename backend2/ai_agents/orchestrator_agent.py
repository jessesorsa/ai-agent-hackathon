import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from ai_agents.hubspot_agent import call_hubspot_agent
from ai_agents.gmail_agent import call_gmail_agent
from ai_agents.slack_agent import call_slack_agent
from ai_agents.calendar_agent import call_calendar_agent
from ai_agents.data_agent import call_data_agent

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

@function_tool
async def call_data_tool(prompt: str) -> str:
    """
    Call the Data agent to handle web search and Notion operations.
    
    Use this tool for:
    - Searching the web for information using Perplexity AI
    - Creating new Notion pages with content
    - Updating existing Notion pages
    - Retrieving information from Notion pages
    - Searching for Notion pages
    - Adding blocks or content to Notion pages
    - Research tasks that require web search and documentation
    
    Args:
        prompt: A natural language request describing the data operation you want to perform.
               Examples: "Search the web for latest AI trends and add them to a Notion page",
               "Create a Notion page with research about quantum computing",
               "Find information about Python best practices and update my Notion notes"
    
    Returns:
        str: The response from the Data agent containing search results, Notion page operations, or combined research and documentation
    """
    return await call_data_agent(prompt)

async def call_orchestrator_agent(prompt: str) -> str:
    """
    Orchestrator agent that routes requests to appropriate agents.
    
    Args:
        prompt: User's request/prompt
    
    Returns:
        str: Response from orchestrator agent
    """
    # Create tools that call the other agents
    tools = [call_hubspot_tool, call_gmail_tool, call_slack_tool, call_calendar_tool, call_data_tool]

    agent = Agent(
        name="Orchestrator",
        instructions="""You are an orchestrator agent that routes requests to appropriate agents.
        - Use call_hubspot_tool for CRM-related requests (searching companies, deals, contacts, creating/updating CRM records)
        - Use call_gmail_tool for all email-related requests (drafting emails, sending emails, fetching emails, summarizing emails)
        - Use call_slack_tool for all Slack-related requests (sending Slack messages, fetching conversation history, looking up users, searching messages)
        - Use call_calendar_tool for all calendar-related requests (creating events, modifying events, finding events, listing events, deleting events)
        - Use call_data_tool for web search and Notion operations (researching topics, creating/updating Notion pages, searching the web)
        - You can use multiple tools if needed to fulfill a request.

I AM: (the current user) Jesse, a co-founder at Capybara AI

UI COMPONENT OUTPUT FORMATTING:
When displaying information, output ONLY valid JSON - no text before or after. The frontend will render visual components based on the JSON structure.

COMPANY CARD (single company details):
Output format: {"role": "company", "content": {"name": "Company Name", "industry": "Software", "icpFit": 85, "domain": "company.com", "website": "https://company.com", "location": "City, State", "employeeCount": "50-100", "revenue": "$5M", "description": "Description"}}
Required: name
Optional: industry, icpFit (0-100), domain, website, location, employeeCount, revenue, description
Use when: Displaying a single company from HubSpot search/creation

EVENT CARD (single event/meeting):
Output format: {"role": "event", "content": {"title": "Event Title", "description": "Description", "timestamp": "2:00 PM", "location": "Location"}}
Required: title
Optional: description, timestamp, location
Use when: Displaying a single calendar event or scheduled meeting

CRITICAL RULES:
- Component JSON = output ONLY the JSON, nothing else
- Regular text responses = output text normally (for explanations, confirmations, etc.)
- Single item → use card format (company/event)
- Multiple items → use table format
- Never mix JSON components with text explanations
- All JSON must be valid and properly formatted""",
        tools=tools,
        model="gpt-4.1-mini"
    )

    result = await Runner.run(
        starting_agent=agent,
        input=prompt,
    )
    
    print(result.final_output)
    return result.final_output