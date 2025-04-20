
# 📝 Text Summariser API

This is a FastAPI-based asynchronous text summarization API that uses Celery and Redis for background processing. The app is deployed on **Render** and provides endpoints for submitting long texts and retrieving concise summaries.

### 🚀 Live Demo
You can test the API live via the FastAPI Swagger UI here:  
👉 [https://text-summariser-1-1.onrender.com/docs](https://text-summariser-1-1.onrender.com/docs)

---

## 📦 Tech Stack

- **FastAPI** – Modern async web framework
- **Celery** – Background task queue
- **Redis** – Message broker for Celery
- **Uvicorn** – ASGI server
- **Render** – Hosting platform for deployment

---

## 🛠️ Installation & Running Locally

### 1. Clone the repo

```bash
git clone https://github.com/Jadavivek/text_summariser_1.git
cd text_summariser_1
```

### 2. Create a virtual environment and activate it

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Redis server (must be installed)

```bash
redis-server
```

### 5. Start Celery worker

```bash
celery -A tasks worker --loglevel=info
```

### 6. Run the FastAPI server

```bash
uvicorn tasks:app --host 0.0.0.0 --port 10000
```

---

## 📌 API Endpoints

### ➕ `POST /summarize/`
Submit a text to summarize.

**Request:**
```json
{
  "text": "Your long text here..."
}
```

**Response:**
```json
{
  "task_id": "e67a1bb3-cb4a-4f3f-b172-xxxxxxxxxxxx"
}
```

---

###  `GET /result/{task_id}`
Get the summary using the task ID.

**Example Response:**
```json
{
  "summary": "Your summarized content goes here."
}
```

---

##  File Structure

```
├── tasks.py             # FastAPI app + Celery tasks
├── requirements.txt     # Project dependencies
├── start.sh             # Render startup script
├── README.md            # Project documentation
```

---

##  Deployment (on Render)

###  Web Service
1. Create a new Web Service on [Render](https://render.com/)
2. Set the start command to:
```bash
./start.sh
```
3. Use `tasks.py` as the entry point (your main FastAPI app).


---

##  Contact

Created by [**Jada Vivek**](https://github.com/Jadavivek)  
Feel free to contribute, fork, or raise issues!

---
