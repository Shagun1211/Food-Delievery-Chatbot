from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_ngrok_skip_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

def get_connection():
    return sqlite3.connect("orders.db", check_same_thread=False)


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            status TEXT,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            food TEXT,
            quantity INTEGER
        )
    """)

    conn.commit()
    conn.close()


create_tables()

def safe_int(val, default=1):
    try:
        return int(val)
    except:
        return default


def get_or_create_order(session_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT order_id FROM orders WHERE session_id=? AND status='active'",
        (session_id,)
    )
    row = cur.fetchone()

    if row:
        conn.close()
        return row[0]

    cur.execute(
        "INSERT INTO orders (session_id, status, created_at) VALUES (?, 'active', ?)",
        (session_id, datetime.now().isoformat())
    )
    conn.commit()
    order_id = cur.lastrowid
    conn.close()
    return order_id


@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        print("INCOMING REQUEST:", data)

        params = (
            data.get("queryResult", {}).get("parameters")
            or data.get("parameters")
            or {}
        )

        session_id = data.get("session", "web-session")

        food = params.get("food")
        quantity = safe_int(params.get("number") or params.get("quantity"))

        if not food:
            return {"fulfillmentText": "Please specify a food item."}

        return add_item(session_id, food.lower(), quantity)

    except Exception as e:
        print("WEBHOOK ERROR:", e)
        return {"fulfillmentText": "Something went wrong. Please try again."}


def add_item(session_id, food, qty):
    order_id = get_or_create_order(session_id)
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT quantity FROM order_items WHERE order_id=? AND food=?",
        (order_id, food)
    )
    row = cur.fetchone()

    if row:
        cur.execute(
            "UPDATE order_items SET quantity = quantity + ? WHERE order_id=? AND food=?",
            (qty, order_id, food)
        )
    else:
        cur.execute(
            "INSERT INTO order_items (order_id, food, quantity) VALUES (?, ?, ?)",
            (order_id, food, qty)
        )

    conn.commit()
    conn.close()

    return {
        "fulfillmentText": f"Added {qty} {food}(s) to your order."
    }
