from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tasks import summarize_text  # Make sure this is properly imported
from celery.result import AsyncResult

app = FastAPI()
cache = {}

class SummarizationRequest(BaseModel):
    text: str

@app.post("/summarize")
async def summarize(request: SummarizationRequest):
    if request.text in cache:
        return {"summary": cache[request.text]}    
    task = summarize_text.delay(request.text)
    return {"task_id": task.id}

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    task = AsyncResult(task_id)
    if task.state == 'PENDING':
        return {"status": "Pending"}
    elif task.state == 'SUCCESS':
        cache[task_id] = task.result  # Cache the result for later use
        return {"status": "Success", "summary": task.result}
    else:
        return {"status": "Failed"}
