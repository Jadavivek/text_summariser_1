import aiohttp
import redis.asyncio as redis
import os

redis_url = os.environ.get("REDIS_URL")
r = redis.from_url(redis_url, decode_responses=True)

GEMINI_API_URL = "https://api.gemini.com/summarize"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

async def summarize_text(text: str) -> str:
    cached = await r.get(text)
    if cached:
        return cached

    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {GEMINI_API_KEY}",
            "Content-Type": "application/json"
        }
        async with session.post(GEMINI_API_URL, json={"text": text}, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                summary = data.get("summary")
                await r.set(text, summary)
                return summary
            else:
                body = await response.text()
                raise Exception(f"Gemini API error: {response.status} - {body}")
