import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from ai_agents.hubspot_agent import call_hubspot_agent
from ai_agents.gmail_agent import call_gmail_agent
from ai_agents.data_agent import call_data_agent

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
async def call_data_tool(prompt: str) -> str:
    """
    Call the Data agent to search the web and manage Notion pages.
    
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
    s
    Returns:
        str: Response from orchestrator agent
    """
    # Create tools that call the other agents
    tools = [call_hubspot_tool, call_gmail_tool, call_data_tool]

    agent = Agent(
        name="Orchestrator",
        instructions="""You are an orchestrator agent that intelligently routes requests to specialized agents and provides rich context.

CRITICAL: Always provide comprehensive context to subagents. Don't just pass the raw user request - enrich it with relevant background information.

ROUTING GUIDELINES:
- Use call_hubspot_tool for CRM-related requests (searching companies, deals, contacts, creating/updating CRM records)
- Use call_gmail_tool for email-related requests (drafting emails, sending emails, fetching emails)
- Use call_data_tool for web search and Notion operations (researching topics, creating/updating Notion pages, searching the web)

CONTEXT ENRICHMENT STRATEGY:
1. Parse the full user request to understand the complete intent and any implicit requirements
2. Extract key entities: company names, contact names, email addresses, deal amounts, dates, topics, etc.
3. When calling subagents, provide enriched prompts that include:
   - The original user request
   - Relevant background context from the conversation
   - Any related information that would help the subagent complete the task
   - Specific requirements or constraints mentioned

EXAMPLES OF GOOD CONTEXT ENRICHMENT:
- User: "Create a deal for Acme Corp"
  → Enriched: "Create a new deal in HubSpot for Acme Corp. Include as much information as possible: company name, domain (extract from company name if needed), industry (default to Software and Technology), deal amount if mentioned, and any other available details."

- User: "Send an email about the meeting"
  → Enriched: "Draft a professional email about the meeting. Include context about what was discussed, next steps, and any relevant details from the conversation. Format it properly with a clear subject line."

- User: "Research AI trends and add to Notion"
  → Enriched: "Search the web for the latest AI trends using Perplexity. Then create or update a Notion page with this research. First search for existing Notion pages about AI trends, retrieve their content, and then add the new research findings."

CHAINING OPERATIONS:
- If a request requires multiple steps, chain the operations intelligently
- For example: Search for a company first, then create a deal associated with that company
- Pass results from one agent call as context to the next agent call when relevant

RESPONSE SYNTHESIS:
- After receiving responses from subagents, synthesize the information clearly
- If multiple agents were used, combine their outputs into a coherent response
- Always provide a clear summary of what was accomplished

Remember: Your role is to be the intelligent coordinator that ensures subagents have all the context they need to succeed.""",
        tools=tools,
        model="gpt-4o-mini"
    )

    result = await Runner.run(
        starting_agent=agent,
        input=prompt,
    )
    
    print(result.final_output)
    return result.final_output