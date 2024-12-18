from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import google.generativeai as genai
import os
from dotenv import load_dotenv
from models import ChatInput, ChatResponse, ResponseModel
from fastapi.templating import Jinja2Templates
import logging
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.gemini import GeminiModel

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()
agent1 = Agent(
    model=GeminiModel('gemini-1.5-flash'),
    system_prompt="You are a helpful customer support agent. Be concise and friendly.",
)

agent2 = Agent(
    model=GeminiModel('gemini-1.5-flash'),
    result_type=ResponseModel,
    system_prompt=(
        "You are an intelligent customer support agent. "
        "Analyze queries carefully and provide structured responses."
    ),
)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_input: ChatInput, request: Request):
    try:
        response = await agent2.run(chat_input.message)
        # response = model.generate_content(chat_input.message)
        ai_message = f"<div class='ai-message'>{response.data}</div>"
        all_messages = f"<div class='all_messages'>{response.data.model_dump_json(indent=2)}</div>"
        cost = f"<div class='cost'>{response.cost()}</div>"
        user_message = f"<div class='user-message'>{chat_input.message}</div>"
        return HTMLResponse(content= user_message + ai_message + all_messages + cost)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)