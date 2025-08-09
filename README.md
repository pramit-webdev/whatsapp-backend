# 📱 WhatsApp Backend (FastAPI + MongoDB)

This is a **WhatsApp-like backend API** built with **FastAPI** and **MongoDB**, designed to handle webhook events, store messages, and send replies.
It can be integrated with a custom frontend to create a full chat application.

---

## 🚀 Features

* Receive **webhook** events from WhatsApp.
* Store messages in **MongoDB**.
* Send messages via API.
* Fetch message history by `wa_id`.
* Ready for **deployment** on Railway, Render, or other cloud providers.

---

## 🐂 Project Structure

```
app/
 ├── db.py               # MongoDB connection
 ├── models.py           # Pydantic models
 ├── routes.py           # API endpoints
 ├── utils.py            # Helper functions
 └── main.py              # FastAPI entry point
```

---

## ⚙️ Requirements

* Python 3.9+
* MongoDB (Atlas or Local)
* pip

---

## 📦 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/whatsapp-backend.git
   cd whatsapp-backend
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file:

   ```env
   MONGO_URI="your_mongodb_connection_string"
   DATABASE_NAME="your_database_name"
   ```

---

## ▶️ Running Locally

```bash
uvicorn app.main:app --reload
```

Server will run on:

```
http://127.0.0.1:8000
```

---

## 🔌 API Endpoints

### 1️⃣ Receive Webhook

```http
POST /webhook
Content-Type: application/json
```

**Sample Payload**

```json
{
  "payload_type": "whatsapp_webhook",
  "_id": "msg1-conv1-xyz",
  "metaData": {
    "device": "android",
    "app_version": "2.24.15"
  },
  "wa_id": "918888888888",
  "messages": [
    {
      "message": "Hello from webhook",
      "sender": "user",
      "timestamp": "2025-08-08T10:00:00Z"
    }
  ]
}
```

---

### 2️⃣ Get Messages

```http
GET /messages/{wa_id}
```

**Example**

```
GET /messages/918888888888
```

---

### 3️⃣ Send Message

```http
POST /messages/send
Content-Type: application/json
```

**Sample Payload**

```json
{
  "wa_id": "918888888888",
  "message": "Hello back!",
  "sender": "system"
}
```

---

## ☁️ Deployment

### **Railway**

1. Push your code to GitHub.
2. Create a new Railway project.
3. Set `MONGO_URI` and `DATABASE_NAME` in Railway Environment Variables.
4. Set **Start Command**:

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

### **Render**

1. Push to GitHub.
2. Create new Web Service.
3. Add `MONGO_URI` & `DATABASE_NAME` in Environment.
4. Start Command:

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

---

## 📜 License

MIT License.
