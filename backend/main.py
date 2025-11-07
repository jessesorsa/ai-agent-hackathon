from fastapi import FastAPI, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from agents.ui_agent import UIAgent
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


@app.post("/ui_agent")
async def ui_agent(request: Request):
    body = await request.json()
    message = body.get("message", "")
    print(f"Received message: {message}")
    agent = UIAgent()
    response = agent.process(prompt=message)
    print(f"Response: {response}")
    return {"message": response}