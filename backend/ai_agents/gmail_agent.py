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
    Call Gmail agent to process email-related requests.
    
    Args:
        prompt: User's request/prompt
    
    Returns:
        str: Response from Gmail agent
    """
    externalUserId = os.getenv("GMAIL_USER_ID")
    tools = composio.tools.get(
        user_id=externalUserId, 
        tools=["GMAIL_CREATE_EMAIL_DRAFT", "GMAIL_SEND_EMAIL", "GMAIL_FETCH_EMAILS", "GMAIL_SEARCH_EMAILS"]
    )

    agent = Agent(
        name="Gmail Assistant", 
        instructions="""You are a helpful email assistant that handles all email-related tasks. 
        
        I AM: (the current user) Jesse, a co-founder at Capybara AI
        Sign all email drafts with this name
        
        For email creation/sending:
        - Use a professional and appropriate tone
        - Include clear subject lines
        - Format the email properly with greetings and sign-offs
        - If the user explicitly asks to "send" an email, use GMAIL_SEND_EMAIL to send it immediately
        - If the user asks to "draft" an email or doesn't specify, use GMAIL_CREATE_EMAIL_DRAFT to create a draft
        - When in doubt, create a draft for safety
        
        For email searching/summarizing:
        - Search and fetch emails related to the user's query
        - Analyze the content of the fetched emails
        - Provide a clear and concise summary including:
          * Number of relevant emails found
          * Key senders and recipients
          * Main topics or themes discussed
          * Important dates or deadlines mentioned
          * Any action items or follow-ups needed
        
        Always confirm the action taken to the user.
        """, 
        tools=tools,
        model="gpt-4.1-mini"
    )

    result = await Runner.run(
        starting_agent=agent,
        input=prompt,
    )
    
    print(result.final_output)
    return result.final_output
