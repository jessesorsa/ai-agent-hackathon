import os
from dotenv import load_dotenv

from composio import Composio
from agents import Agent, Runner
from composio_openai_agents import OpenAIAgentsProvider

# Load environment variables
load_dotenv()

composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"), provider=OpenAIAgentsProvider())

 
async def call_slack_agent(prompt: str) -> str:
    """
    Call Slack agent to process Slack-related requests.
    
    Args:
        prompt: User's request/prompt
    
    Returns:
        str: Response from Slack agent
    """
    externalUserId = os.getenv("SLACK_USER_ID", "default-user")
    tools = composio.tools.get(
        user_id=externalUserId, 
        tools=[
            # User lookup
            "SLACK_USERS_LOOKUP_BY_EMAIL",
            "SLACK_USERS_INFO",
            "SLACK_USERS_LIST",
            
            # Channel management
            "SLACK_CONVERSATIONS_LIST",
            "SLACK_CONVERSATIONS_INFO",
            "SLACK_CONVERSATIONS_HISTORY",
            "SLACK_CONVERSATIONS_MEMBERS",
            
            # Messaging
            "SLACK_CHAT_POST_MESSAGE",
            "SLACK_CHAT_UPDATE",
            "SLACK_CHAT_DELETE",
            
            # DM management
            "SLACK_CONVERSATIONS_OPEN",  # Open/create DM
            
            # Search
            "SLACK_SEARCH_MESSAGES",
        ]
    )

    agent = Agent(
        name="Slack Assistant", 
        instructions="""You are a helpful Slack assistant that handles all Slack-related tasks.
        
        For user lookup:
        - Use SLACK_USERS_LOOKUP_BY_EMAIL to find a user by their email address
        - Use SLACK_USERS_INFO to get detailed information about a user by their user ID
        - Use SLACK_USERS_LIST to list all users in the workspace
        
        For fetching conversation history by email:
        1. First use SLACK_USERS_LOOKUP_BY_EMAIL to get the user ID from their email
        2. Then use SLACK_CONVERSATIONS_OPEN to open/get the DM channel with that user
        3. Finally use SLACK_CONVERSATIONS_HISTORY with the channel ID to fetch messages
        
        For channel operations:
        - Use SLACK_CONVERSATIONS_LIST to list all channels
        - Use SLACK_CONVERSATIONS_INFO to get channel details
        - Use SLACK_CONVERSATIONS_HISTORY to fetch message history from a channel
        - Use SLACK_CONVERSATIONS_MEMBERS to see who's in a channel
        
        For sending messages:
        - Use SLACK_CHAT_POST_MESSAGE to send a new message to a channel or DM
        - To send a DM by email: first lookup user ID, then open DM channel, then post message
        - Use SLACK_CHAT_UPDATE to edit an existing message
        - Use SLACK_CHAT_DELETE to delete a message
        
        For searching:
        - Use SLACK_SEARCH_MESSAGES to search for messages across the workspace
        
        Important notes:
        - Slack uses user IDs (UXXXXXXX format), not emails directly for most operations
        - Always map email → user ID first when working with emails
        - DM channels have IDs that start with 'D'
        - Group DMs start with 'G'
        - Public channels start with 'C'
        - Handle pagination for history and lists (use cursor parameter)
        
        Always confirm the action taken to the user and provide relevant details.
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
