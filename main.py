# main.py
from fastapi import FastAPI, BackgroundTasks
from tasks import summarize_text
import uuid

app = FastAPI()

# In-memory task results (optional: replace with Redis or DB)
summaries = {}
@app.get("/")
def health_check():
    return {"status": "alive", "docs": "/docs"}
@app.api_route("/", methods=["GET", "HEAD"])
async def health_check(request: Request):
    return {"status": "alive", "docs": "/docs"}

@app.post("/summarize/")
async def summarize(text: str, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    summaries[task_id] = "Processing..."

    async def process():
        result = await summarize_text(text)
        summaries[task_id] = result

    background_tasks.add_task(process)
    return {"task_id": task_id}

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    return {"summary": summaries.get(task_id, "Task ID not found")}
