from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import google.generativeai as genai
import os
from dotenv import load_dotenv
from models import ChatInput, ChatResponse
from fastapi.templating import Jinja2Templates
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

app = FastAPI()
model = genai.GenerativeModel('gemini-pro')

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_input: ChatInput, request: Request):
    try:
        response = model.generate_content(chat_input.message)
        ai_message = f"<div class='ai-message'>{response.text}</div>"
        user_message = f"<div class='user-message'>{chat_input.message}</div>"
        return HTMLResponse(content= user_message + ai_message)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)