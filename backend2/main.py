from fastapi import FastAPI, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from ai_agents.hubspot_agent import call_hubspot_agent
from ai_agents.gmail_agent import call_gmail_agent
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Add CORS middleware - allow all origins (development only!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/hubspot_agent")
async def hubspot_agent(request: Request):
    body = await request.json()
    message = body.get("message", "")
    print(f"Received message: {message}")
    response = await call_hubspot_agent(message)
    print(f"Response: {response}")
    return {"message": response}


@app.post("/gmail_agent")
async def gmail_agent(request: Request):
    body = await request.json()
    message = body.get("message", "")
    print(f"[Gmail Agent] Received message: {message}")
    response = await call_gmail_agent(message)
    print(f"[Gmail Agent] Response: {response}")
    return {"message": response}