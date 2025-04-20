
from celery import Celery
import requests
app = Celery('tasks',
             broker='rediss://:password@your_redis_internal_url:6379/0',
             backend='rediss://:password@your_redis_internal_url:6379/0')

cache = {}
GEMINI_API_URL = "https://api.gemini.com/summarize"
GEMINI_API_KEY = "AIzaSyCjbPgV1PRpRksTMt0MiW884pRe2bYExtA"
def summarize_text(text):
    if text in cache:
        return cache[text]
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(GEMINI_API_URL, json={"text": text}, headers=headers)
    if response.status_code == 200:
        summary = response.json().get("summary")
        cache[text] = summary
        return summary
    else:
        raise Exception(f"Gemini API failed: {response.status_code} - {response.text}")
