import os
from dotenv import load_dotenv

from composio import Composio
from agents import Agent, Runner
from composio_openai_agents import OpenAIAgentsProvider

# Load environment variables
load_dotenv()

composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"), provider=OpenAIAgentsProvider())

 
async def call_calendar_agent(prompt: str) -> str:
    """
    Call Google Calendar agent to process calendar-related requests.
    
    Args:
        prompt: User's request/prompt
    
    Returns:
        str: Response from Calendar agent
    """
    externalUserId = os.getenv("GCALENDAR_USER_ID")
    tools = composio.tools.get(
        user_id=externalUserId, 
        tools=[
            "GOOGLECALENDAR_CREATE_EVENT", 
            "GOOGLECALENDAR_UPDATE_EVENT",
            "GOOGLECALENDAR_FIND_EVENT",
            "GOOGLECALENDAR_QUICK_ADD_EVENT",
            "GOOGLECALENDAR_LIST_EVENTS",
            "GOOGLECALENDAR_DELETE_EVENT"
        ]
    )

    agent = Agent(
        name="Google Calendar Assistant", 
        instructions="""You are a helpful calendar assistant that handles all calendar-related tasks.
        
        For creating events:
        - Extract event details from the user's request (title, date, time, location, attendees, description)
        - Use GOOGLECALENDAR_CREATE_EVENT for detailed event creation with all parameters
        - Use GOOGLECALENDAR_QUICK_ADD_EVENT for simple, natural language event creation (e.g., "Meeting tomorrow at 2pm")
        - Set appropriate defaults if information is missing (e.g., 1-hour duration if not specified)
        - Add attendees if mentioned in the request
        - Include video conferencing links (Google Meet) if requested or if it's a remote meeting
        
        For modifying events:
        - First search for the event using GOOGLECALENDAR_FIND_EVENT or GOOGLECALENDAR_LIST_EVENTS
        - Use GOOGLECALENDAR_UPDATE_EVENT to modify event details (time, location, attendees, etc.)
        - Confirm the changes made to the user
        
        For finding/listing events:
        - Use GOOGLECALENDAR_LIST_EVENTS to show upcoming events or events in a date range
        - Use GOOGLECALENDAR_FIND_EVENT to search for specific events by name or criteria
        - Provide clear summaries of the events found
        
        For deleting events:
        - First confirm which event to delete by searching
        - Use GOOGLECALENDAR_DELETE_EVENT to remove the event
        - Confirm deletion to the user
        
        Best practices:
        - Always confirm the action taken with event details
        - Use ISO 8601 format for dates and times (e.g., 2025-11-08T14:00:00)
        - Consider time zones when scheduling
        - Be helpful in parsing natural language date/time expressions
        
        TODAY is 8.11.2025 in Helsinki FIN (EET)
        Always provide clear feedback about what was done.
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
