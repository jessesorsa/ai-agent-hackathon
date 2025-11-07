import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables before creating client
load_dotenv()

# Initialize the client once at module level (like the example)
client = OpenAI(
    api_key=os.environ.get("THESYS_API_KEY"),
    base_url="https://api.thesys.dev/v1/embed"
)


def call_llm(
    prompt: str,
    model: str = "c1-4o-mini",
    temperature: float = 0.7,
    max_tokens: int = None,
    system_prompt: str = None
) -> str:
    """
    Simple function to call Thesys C1 API with a single prompt.
    """
    # Prepare messages
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    # Make the API call
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    return completion.choices[0].message.content


class UIAgent:
    """
    Basic UI Agent that uses Thesys C1 API.
    """
    
    DEFAULT_SYSTEM_PROMPT = "You create UIs."
    
    def __init__(self, model: str = "c1-4o-mini", temperature: float = 0.7):
        self.model = model
        self.temperature = temperature
    
    def process(self, prompt: str, system_prompt: str = None) -> str:
        final_system_prompt = system_prompt if system_prompt is not None else self.DEFAULT_SYSTEM_PROMPT
        
        return call_llm(
            prompt=prompt,
            model=self.model,
            temperature=self.temperature,
            system_prompt=final_system_prompt
        )