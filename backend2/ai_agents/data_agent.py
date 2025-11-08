import os
from dotenv import load_dotenv
import os

from composio import Composio
from agents import Agent, Runner
from composio_openai_agents import OpenAIAgentsProvider

# Load environment variables
load_dotenv()

composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"), provider=OpenAIAgentsProvider())

 
async def call_data_agent(prompt: str) -> str:
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
        tools=[
            "PERPLEXITYAI_PERPLEXITY_AI_SEARCH",  # Web search
            "NOTION_CREATE_NOTION_PAGE",                  # Create Notion pages
            "NOTION_FETCH_BLOCK_CONTENTS",                     # Get Notion page content
            "NOTION_FETCH_DATA",                 # Search Notion pages
            "NOTION_APPEND_BLOCK_CHILDREN",        # Add blocks to pages
        ])

    agent = Agent(
        name="Data agent", 
        instructions="""You are a helpful assistant that can search the web and manage Notion pages.

IMPORTANT WORKFLOW FOR NOTION OPERATIONS:
1. When working with existing Notion pages, ALWAYS search for pages first using NOTION_FETCH_DATA to find the page ID
2. Use the search results to identify the correct page by name or title
3. Extract the page ID from the search results
4. ALWAYS retrieve the full page content using NOTION_FETCH_BLOCK_CONTENTS with the page ID to see what's already in the page
5. Review the existing content to understand the page structure and avoid duplicating information
6. Use the page ID and content understanding for subsequent operations like NOTION_APPEND_BLOCK_CHILDREN

WORKFLOW:
- For web research: Use PERPLEXITYAI_PERPLEXITY_AI_SEARCH to find information
- For creating new pages: Use NOTION_CREATE_NOTION_PAGE (no search or content fetch needed)
- For updating existing pages: 
  1. Search with NOTION_FETCH_DATA to find the page ID
  2. Retrieve full content with NOTION_FETCH_BLOCK_CONTENTS to see existing content
  3. Then use NOTION_APPEND_BLOCK_CHILDREN with the page ID to add new content
- For adding content to existing pages: 
  1. Search with NOTION_FETCH_DATA to find the page ID
  2. Retrieve full content with NOTION_FETCH_BLOCK_CONTENTS to understand existing structure
  3. Use NOTION_APPEND_BLOCK_CHILDREN with the page ID to add new blocks

CRITICAL: Always fetch and review page content before modifying existing pages. Never operate on a page without first retrieving its full content.""", 
        tools=tools,
        model="gpt-4o-mini"
    )

    result = await Runner.run(
        starting_agent=agent,
        input=prompt,
    )
    
    print(result.final_output)
    return result.final_output