# 💑 AI Relationship Counseling Engine

A production-ready, highly scalable FastAPI web application backend for shared and individual relationship e-counseling. This architecture implements a multi-tier memory structure, keeping track of rolling profiles, active triggers, recurring issues, and agreements asynchronously.

## 🚀 Project Features

- **FastAPI Core**: High performance, automated interactive Swagger/OpenAPI documentation.
- **Multi-Level Context Memory**: Real-time structured JSON state updates isolated per couple.
- **Asynchronous Pipeline Workers**: Offloads heavy linguistic feature extraction to Python background execution workers, minimizing api response latency.
- **Type-Safe Payloads**: Robust runtime validation using Pydantic.
- **Ready to Deploy**: Preconfigured out-of-the-box support for platforms like **Railway** and **Render** via standard `Procfile` configurations.

---

## 📂 Repository File Index

* **`main.py`**: The central entry point, defining schemas, asynchronous extraction processes, and api routing controllers.
* **`Procfile`**: Process configuration mapping web execution commands for hosting platforms.
* **`requirements.txt`**: Complete set of Python dependency pins.
* **`README.md`**: Core system setup and testing guides.

---

## 🛠 Quick Start Guide

### 1. Run Locally
Make sure Python 3.10+ is installed on your local workstation.
```bash
# Clone and enter the repository folder
git clone https://github.com/zeeshanali786/e-consuler.git
cd e-consuler

# Install required dependencies
pip install -r requirements.txt

# Launch the local Uvicorn development server
uvicorn main:app --reload
```
Once the server starts up, navigate to **`http://127.0.0.1:8000/docs`** to explore the interactive API UI!

---

## 📡 Interactive Endpoints & Schemas

### `POST /session/start`
- **Purpose**: Instantiates a clean, unique counseling profile identifier for a couple.
- **Response Output**:
  ```json
  {
    "couple_id": "couple_session_e9a11c",
    "status": "initialized"
  }
  ```

### `POST /chat`
- **Purpose**: Posts incoming chat messages from either partner. Triggers non-blocking background analysis of relationship data and returns empathetic feedback.
- **Payload Input**:
  ```json
  {
    "couple_id": "couple_session_e9a11c",
    "sender": "Husband",
    "message": "It upsets me when you ignore my text messages."
  }
  ```
- **Response Output**:
  ```json
  {
    "counselor_response": "[AI Counselor API]: I notice that trigger 'you ignore my text messages' is arising right now...",
    "timestamp": "2026-11-12T03:00:00.000000Z"
  }
  ```

### `GET /profile/{couple_id}`
- **Purpose**: Fetches the structured, continuously updated rolling JSON metadata containing active triggers and resolutions.
- **Response Output**:
  ```json
  {
    "couple_id": "couple_session_e9a11c",
    "recurring_conflicts": [],
    "agreed_homework": [],
    "partner_a_triggers": ["you ignore my text messages"],
    "partner_b_triggers": [],
    "last_updated": "2026-11-12T03:00:05.123456Z"
  }
  ```

---

## ☁ Deploying to Railway (One-Click Setup)

1. Sign up at [Railway.app](https://railway.app).
2. Click **New Project** -> **Deploy from GitHub repository**.
3. Link your GitHub account and select your **`e-consuler`** repository.
4. Click **Deploy Now**.
5. Once the build step concludes, open the service panel -> click **Settings** -> under **Public Networking**, select **Generate Domain**.
6. Congratulations! Your HTTPS server URL is live and public!
