from fastapi import FastAPI, BackgroundTasks, Request
import uuid
from summarizer import summarize_text

app = FastAPI()

# Store summaries temporarily (replace with DB in production)
summaries = {}

@app.post("/summarize/")
async def summarize(text: str, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())  # use UUID for tracking
    summaries[task_id] = "Processing..."

    async def process():
        result = await summarize_text(text)
        summaries[task_id] = result

    background_tasks.add_task(process)
    return {"task_id": task_id}

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    return {"summary": summaries.get(task_id, "Task ID not found")}

@app.api_route("/", methods=["GET", "HEAD"])
async def health_check(request: Request):
    return {"status": "alive", "docs": "/docs"}
