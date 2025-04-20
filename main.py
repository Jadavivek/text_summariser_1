from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import requests
import os
from typing import Optional

# Initialize FastAPI app
app = FastAPI()

# Set up cache (you can use Redis here too, but it's optional for now)
cache = {}
GEMINI_API_URL = "https://api.gemini.com/summarize"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Pydantic model for incoming summarization request
class SummarizationRequest(BaseModel):
    text: str

# Function to handle text summarization (without Celery)
def summarize_text(text: str):
    if text in cache:
        return cache[text]
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(GEMINI_API_URL, json={"text": text}, headers=headers)
    if response.status_code == 200:
        summary = response.json().get("summary")
        cache[text] = summary  # Cache the result
        return summary
    else:
        raise Exception(f"Gemini API failed: {response.status_code} - {response.text}")

# Route to initiate the summarization task
@app.post("/summarize/")
async def summarize(request: SummarizationRequest, background_tasks: BackgroundTasks):
    # Start the background task to summarize text
    background_tasks.add_task(summarize_text, request.text)
    return {"message": "Summarization is in progress"}

# Route to get cached summary (if exists)
@app.get("/summary/")
async def get_summary(request: SummarizationRequest):
    summary = cache.get(request.text)
    if summary:
        return {"summary": summary}
    else:
        raise HTTPException(status_code=404, detail="Summary not found")
