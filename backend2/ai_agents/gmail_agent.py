import os
from dotenv import load_dotenv

from composio import Composio
from agents import Agent, Runner
from composio_openai_agents import OpenAIAgentsProvider

# Load environment variables
load_dotenv()

composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"), provider=OpenAIAgentsProvider())

 
async def call_gmail_agent(prompt: str) -> str:
    """
    Call Gmail agent to draft emails based on user prompts.
    
    Args:
        prompt: User's request/prompt for email drafting
    
    Returns:
        str: Response from Gmail agent with drafted email
    """
    # Get Gmail tools that are pre-configured
    externalUserId = os.getenv("GMAIL_USER_ID")
    tools = composio.tools.get(
        user_id=externalUserId, 
        tools=["GMAIL_CREATE_EMAIL_DRAFT", "GMAIL_SEND_EMAIL", "GMAIL_FETCH_EMAILS"]
    )

    agent = Agent(
        name="Gmail Assistant", 
        instructions="""You are a helpful email assistant that drafts professional emails based on user requests. 
        When drafting emails:
        - Use a professional and appropriate tone
        - Include clear subject lines
        - Format the email properly with greetings and sign-offs
        - Ask for clarification if needed (recipient, subject, specific details)
        """, 
        tools=tools
    )

    result = await Runner.run(
        starting_agent=agent,
        input=prompt,
    )
    
    print(result.final_output)
    return result.final_output
