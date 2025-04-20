# tasks.py
import os
import aiohttp
import redis.asyncio as redis

GEMINI_API_URL = "https://api.gemini.com/summarize"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Use Redis for cache
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.from_url(redis_url, decode_responses=True)

async def summarize_text(text: str) -> str:
    # Check Redis cache
    cached_summary = await r.get(text)
    if cached_summary:
        return cached_summary

    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(GEMINI_API_URL, json={"text": text}, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                summary = data.get("summary")
                await r.set(text, summary)  # Cache result
                return summary
            else:
                raise Exception(f"Gemini API failed: {resp.status} - {await resp.text()}")
