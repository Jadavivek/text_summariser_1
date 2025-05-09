from fastapi import FastAPI, BackgroundTasks
from tasks import summarize_text
import uuid

app = FastAPI()

# Store summaries temporarily (replace with DB in production)
summaries = {}

@app.get("/")
async def root():
    return {"message": "Welcome to the Text Summarizer API. Please visit /docs to interact with the API."}

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
