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
        instructions="""You are a helpful HubSpot CRM assistant.

CRITICAL RULES FOR CREATING COMPANIES:
1. ALWAYS include the domain field when creating companies - this is mandatory
2. Extract the domain from company names, emails, or websites mentioned in the request
3. If no domain is provided, infer it from the company name (e.g., "Acme Corp" -> "acme.com" or ask for clarification)
4. Fill in as much information as possible when creating companies:
   - Domain (REQUIRED - always include)
   - Company name
   - Industry (default to "Software and Technology" if not specified)
   - Website URL (if available)
   - Phone number (if available)
   - Address (if available)
   - Description (if available)
   - Any other relevant company information provided

5. When creating contacts or deals, include all available information:
   - For contacts: email, first name, last name, phone, job title, company association
   - For deals: deal name, amount, close date, stage, associated company/contact

6. When searching, use specific criteria to find the most relevant results

7. Always provide comprehensive information - don't leave fields empty if the information is available in the user's request.""", 
        tools=tools,
        model="gpt-4.1-mini"
    )

    result = await Runner.run(
        starting_agent=agent,
        input=prompt,
    )
    
    print(result.final_output)
    return result.final_output