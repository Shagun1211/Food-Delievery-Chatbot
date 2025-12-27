# Food-Delievery-Chatbot

🍕 Food-Delievery-Chatbot

A full-stack food delivery chatbot built using FastAPI, SQLite, and a web-based frontend, capable of taking food orders via natural language, storing them in a database, and responding in real time.
The chatbot supports browser-based interaction as well as Dialogflow integration.


🚀 Features

🗣️ Natural language food ordering (e.g., “add 2 pizza”)

⚡ FastAPI-based REST webhook

🌐 Web chatbot UI using HTML, CSS, and JavaScript

🧠 Dialogflow-compatible webhook structure

💾 SQLite database for persistent order storage

🔁 Session-based order management

🔐 CORS-enabled API for frontend integration

🌍 ngrok support for public webhook exposure


🛠️ Tech Stack
Backend

Python

FastAPI

SQLite

Uvicorn

ngrok

Frontend

HTML

CSS

JavaScript (Fetch API)

NLP / Chat Interface

Dialogflow (optional integration)

Custom rule-based parsing for browser UI


🧠 How It Works

User sends a message via UI or Dialogflow

Request reaches FastAPI /webhook

Parameters are extracted safely

Order is stored/updated in SQLite

Response is returned as chatbot reply


🔒 Error Handling

Safe JSON parsing

Graceful fallback responses

Database integrity checks

Frontend + backend compatibility


🎯 Use Cases

Food ordering systems

Chatbot backend learning

NLP + API integration projects

College mini/major project

Resume-ready full-stack application


📌 Future Enhancements

🧾 Bill generation

❌ Remove / update items

📦 Order status tracking

📱 WhatsApp / Telegram bot integration

⚛️ React-based frontend

🧠 ML-based intent detection
