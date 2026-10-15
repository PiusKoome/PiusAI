import sqlite3
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Import database helpers and your AI engine
from database import init_db, save_message, load_chat_history
from chat import generate_response

app = FastAPI(title="Pius AI Server")
templates = Jinja2Templates(directory="templates")

# Initialize database table on server startup
init_db()


class ChatRequest(BaseModel):
    prompt: str


def process_chat(user_input: str) -> str:
    # 1. Save user's incoming message to DB
    save_message("user", user_input)

    # 2. Pull previous context from SQLite
    full_context = load_chat_history(limit=20)

    # 3. Generate response using your chat logic module
    ai_reply = generate_response(user_input)

    # 4. Save AI's response to DB
    save_message("assistant", ai_reply)

    return ai_reply


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/history")
def get_history():
    """Returns stored chat history to populate the frontend sidebar."""
    conn = sqlite3.connect("pius_ai.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM chat_history ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()

    history = [{"role": row["role"], "content": row["content"]} for row in rows]
    return {"history": history}


@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    reply = process_chat(request.prompt)
    return {"reply": reply}


# Run locally with Uvicorn when executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)