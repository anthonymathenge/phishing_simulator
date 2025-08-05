from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import sqlite3
import uuid
import os
import json
from email_utils import send_phishing_email
from typing import List

app = FastAPI()

# CORS config — allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set frontend origin here in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === DATABASE INIT ===
DB_PATH = "phishing.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id TEXT PRIMARY KEY,
            email TEXT,
            opened BOOLEAN DEFAULT 0,
            clicked BOOLEAN DEFAULT 0,
            submitted BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# === API ROUTES ===
def store_user(user_id: str, email: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO interactions (id, email) VALUES (?, ?)", (user_id, email))
    conn.commit()
    conn.close()
    
TEMPLATE_FILE = "email_template.json"


@app.post("/template/save")
async def save_template(subject: str = Form(...), body: str = Form(...)):
    with open("email_template.json", "w") as f:
        json.dump({"subject": subject, "body": body}, f)
    return {"status": "saved"}

@app.get("/template/load")
async def load_template():
    if os.path.exists(TEMPLATE_FILE):
        with open(TEMPLATE_FILE, "r") as f:
            return json.load(f)
    return {"subject": "", "body": ""}

@app.post("/send_campaign/")
async def send_campaign(email_list: List[str] = Form(...), template_html: str = Form(...)):
    results = {"sent": [], "failed": []}
    for email in email_list:
        user_id = str(uuid.uuid4())
        try:
            send_phishing_email(email, user_id)
            store_user(user_id, email)
            results["sent"].append(email)
        except Exception as e:
            print(f"[✗] Failed to send to {email}: {e}")
            results["failed"].append({"email": email, "error": str(e)})
    return results

@app.get("/track/{user_id}")
async def track_open(user_id: str):
    update_interaction(user_id, "opened")
    return FileResponse("static/tracker.png", media_type="image/png")

@app.get("/click/{user_id}")
async def track_click(user_id: str):
    update_interaction(user_id, "clicked")
    return RedirectResponse(url=f"/fake-login?uid={user_id}")

@app.get("/fake_login", response_class=HTMLResponse)
async def serve_fake_login():
    with open("templates/fake_login.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/fake_survey", response_class=HTMLResponse)
async def serve_fake_survey():
    with open("templates/fake_survey.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/fake_update", response_class=HTMLResponse)
async def serve_fake_update():
    with open("templates/fake_update.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/fake_download", response_class=HTMLResponse)
async def serve_fake_download():
    with open("templates/fake_download.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/submit")
async def handle_form(uid: str = Form(...), username: str = Form(...), password: str = Form(...)):
    update_interaction(uid, "submitted")
    # Log credentials — ethically simulate, don't use real data in production!
    print(f"[!] {uid} submitted: {username} / {password}")
    return {"message": "Thank you. You may now close this window."}

@app.get("/tracking_data")
def get_tracking_data():
    conn = sqlite3.connect("phishing.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interactions")  # Make sure this table exists
    rows = cursor.fetchall()
    conn.close()

    result = [
        {
            "user_id": row[0],
            "event": row[1],
            "timestamp": row[2]
        }
        for row in rows
    ]
    return JSONResponse(content=result)

# === DB HELPERS ===

def store_user(user_id: str, email: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO interactions (id, email) VALUES (?, ?)", (user_id, email))
    conn.commit()
    conn.close()

def update_interaction(user_id: str, action: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"UPDATE interactions SET {action} = 1 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
