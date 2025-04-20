from fastapi import FastAPI, BackgroundTasks, Request
import uuid
from tasks import summarize_text
app = FastAPI()
summaries = {}
async def summarize(text: str, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())  # use UUID for tracking
    summaries[task_id] = "Processing..."

    async def process():
        result = await summarize_text(text)
        summaries[task_id] = result

    background_tasks.add_task(process)
    return {"task_id": task_id}
async def get_result(task_id: str):
    return {"summary": summaries.get(task_id, "Task ID not found")}

async def health_check(request: Request):
    return {"status": "alive", "docs": "/docs"}
