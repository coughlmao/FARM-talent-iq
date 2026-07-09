# Interview Platform

A modern full-stack **Interview Platform** built using the **FARM Stack
(FastAPI + React + MongoDB)** with real-time video rooms, live chat, and
a Monaco-based coding environment. The platform enables candidates and
interviewers to conduct technical interviews seamlessly with automated
evaluation and real-time collaboration.

------------------------------------------------------------------------

## Table of Contents

-   Project Overview
-   Features
-   Tech Stack
-   Local Setup
-   Deployment on Render
-   How It Works
-   Important Notes
-   Troubleshooting
-   License

------------------------------------------------------------------------

## Project Overview

The **Interview Platform** is a full-stack web application designed to simplify the technical interview process. It provides a modern, real-time environment where interviewers can create coding interview sessions and candidates can join and solve problems together with video conferencing and live chat.

The platform integrates **Clerk for authentication**, **Stream.io for video/chat infrastructure**, and **Inngest for background job processing**. Code execution is sandboxed through the **Piston API**, ensuring security and isolation.

### Key Highlights

✨ **Authentication & Authorization**
-   Secure OAuth/email login via Clerk\
-   Automatic user sync from Clerk to MongoDB via Inngest webhooks\
-   JWT-based API authentication

🎥 **Real-time Communication**
-   HD video conferencing powered by Stream.io\
-   Live text chat during interviews\
-   Seamless session management

💻 **Coding Interview Environment**
-   Monaco Editor (VS Code-like experience)\
-   Support for JavaScript, Python, and Java\
-   Code execution via Piston API (secure, isolated sandboxes)\
-   Pre-loaded coding problem library with test cases

📊 **Dashboard & Analytics**
-   Browse active interview sessions\
-   View completed session history\
-   Search and filter coding problems by difficulty\
-   Real-time session statistics

🚀 **Production-Ready**
-   Fully deployed on Render with `render.yaml` configuration\
-   Async-first backend (FastAPI + Beanie)\
-   Optimized frontend build with Vite\
-   Comprehensive error handling and logging

------------------------------------------------------------------------

## Features

### Authentication & Authorization

-   **OAuth/Email Login**: Secure authentication via Clerk\
-   **Automatic User Sync**: Inngest webhooks auto-create users in MongoDB on signup\
-   **JWT Validation**: All API routes protected with Clerk JWT verification\
-   **Automatic Cleanup**: Users are deleted from MongoDB when account is removed from Clerk\
-   **Session Management**: Clerk handles secure token management and refresh

------------------------------------------------------------------------

### Interview Sessions

-   **Create Sessions**: Interviewers create sessions for specific coding problems\
-   **1-on-1 Sessions**: Maximum 2 participants per session (host + candidate)\
-   **Unique Room Links**: Each session generates a shareable link for candidates\
-   **Session Status Tracking**: Sessions tracked as "active" or "completed"\
-   **Real-time Notifications**: Live updates via Stream SDK\

------------------------------------------------------------------------

### Real-time Communication

-   **Video Conferencing**: HD video/audio powered by Stream.io\
-   **Live Chat**: In-session messaging between participants\
-   **Co-viewer Experience**: Both users see the same problem and code editor\

------------------------------------------------------------------------

### Coding Environment

-   **Monaco Editor Integration**: Full VS Code-like editing experience\
-   **Multi-language Support**: JavaScript (18.15.0), Python (3.10.0), Java (15.0.2)\
-   **Secure Code Execution**: Code runs in isolated Piston API sandboxes (not on your server)\
-   **Real-time Output**: Instant execution results and error messages\
-   **Problem Library**: Pre-loaded coding problems with starter code and test cases\

------------------------------------------------------------------------

### Dashboard & Analytics

-   **Welcome Section**: Personalized greeting with quick-action buttons\
-   **Active Sessions**: Browse and join available interview sessions\
-   **Recent Sessions**: View history of completed interviews\
-   **User Stats**: Display total sessions, completion counts, etc.\
-   **Problem Browser**: Browse available coding problems by difficulty\

------------------------------------------------------------------------

### Background Workflows (Inngest)

-   **User Creation**: Auto-sync Clerk signups to MongoDB\
-   **User Deletion**: Auto-cleanup when users are removed from Clerk\
-   **Event Processing**: Webhook-based asynchronous job handling\
-   **Scalable Background Jobs**: Decoupled from request-response cycle

------------------------------------------------------------------------

## Tech Stack

### Backend (Python 3.12)

-   **Framework**: FastAPI 0.128.0\
-   **Database**: MongoDB with Beanie ODM 2.0.1\
-   **Authentication**: Clerk Backend API 4.2.0\
-   **Background Jobs**: Inngest 0.5.13\
-   **Code Execution**: Piston API (external code execution service)\
-   **Video/Chat**: Stream SDK 2.5.21\
-   **Server**: Gunicorn 23.0.0 with UvicornWorker\
-   **Linting**: Ruff\
-   **API Type**: REST APIs

------------------------------------------------------------------------

### Frontend

-   **Framework**: React 19.2.0\
-   **Build Tool**: Vite 7.3.0\
-   **Router**: React Router 7.11.0\
-   **Data Fetching**: TanStack React Query 5.90.12\
-   **Code Editor**: Monaco Editor 4.7.0\
-   **Video/Chat SDK**: Stream SDK (react) 13.13.1\
-   **Styling**: TailwindCSS 4.1.18 + daisyUI 5.5.14\
-   **UI Components**: Lucide React (icons), react-hot-toast (notifications)\
-   **Layout**: React Resizable Panels 4.0.15\
-   **HTTP Client**: Axios 1.13.2\
-   **Authentication**: Clerk React 5.59.0\
-   **Utilities**: date-fns, canvas-confetti

------------------------------------------------------------------------

### Deployment & Infrastructure

-   **Deployment**: Render (with render.yaml configuration)\
-   **Video/Chat/Messaging**: Stream.io\
-   **Authentication**: Clerk\
-   **Background Jobs**: Inngest\
-   **Version Control**: Git

------------------------------------------------------------------------

## Local Setup

### Prerequisites

- Node.js (v16+), Python (v3.12), MongoDB, Git
- Clerk, Stream.io, and Inngest accounts with API keys

### Backend Setup

```bash
cd backend
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
uv sync
```

Create `.env` in `backend/`:
```bash
MONGO_URI=mongodb+srv://...
CLERK_SECRET_KEY=your_key
CLERK_FRONTEND_API=your_url
STREAM_API_KEY=your_key
STREAM_API_SECRET=your_secret
INNGEST_EVENT_KEY=your_key
INNGEST_SIGNING_KEY=your_key
ENV_TYPE=development
```

Start:
```bash
uv run fastapi dev app/main.py
```

Backend: http://localhost:8000 | Docs: http://localhost:8000/docs

### Frontend Setup

```bash
cd frontend
npm install
```

Create `.env` in `frontend/`:
```bash
VITE_API_BASE_URL=http://localhost:8000
VITE_CLERK_PUBLISHABLE_KEY=your_key
VITE_STREAM_API_KEY=your_key
```

Start:
```bash
npm run dev
```

Frontend: http://localhost:5173

------------------------------------------------------------------------

## How It Works

1. **User Authentication**: OAuth login via Clerk, JWT validation, user synced to MongoDB
2. **Create Session**: Host selects a problem, generates unique session link, creates Stream call & chat
3. **Join Session**: Candidate joins via link, both users connected to video/chat
4. **Live Interview**: Monaco editor with code execution via Piston API, real-time chat
5. **End Session**: Marks as completed, updates dashboard

**Architecture**: Clerk JWT → Validate via JWKS → MongoDB lookup → Stream.io (video/chat) → Piston API (code execution)

------------------------------------------------------------------------

## Deployment

### Render (Recommended)

The project includes `render.yaml` for one-click deployment:

1. Push to GitHub
2. Connect repo to Render dashboard
3. Add environment variables (MONGO_URI, CLERK_*, STREAM_*, INNGEST_*)
4. Deploy — Render auto-detects `render.yaml` and builds both backend & frontend

**Result**: Single service at `https://your-app.onrender.com` serving API + frontend

------------------------------------------------------------------------

## Important Notes

- **Security**: Never commit `.env` — use environment variables. Sign requests with Clerk JWT. Piston API sandboxes code execution.
- **MongoDB Atlas**: Use Atlas in production (not local MongoDB)
- **Clerk Setup**: Configure OAuth providers and webhook URL: `{backend-url}/api/inngest`
- **Render Free**: Service sleeps after 15 min inactivity. Use paid plan for production.
- **Development**: `fastapi dev app/main.py` and `npm run dev` support hot reload

------------------------------------------------------------------------

## Project Structure

```
backend/
  ├── app/
  │   ├── /api
  │   ├── /core             # Routes
  │   ├── /dependencies     # Auth
  │   ├── /integrations     # 3rd Party Services
  │   ├── /models           # MongoDB Models
  │   ├── /repositories     # MongoDB Operations
  │   ├── /schemas          # Pydantic schemas
  │   ├── /services         # Business Logic
  │   └── main.py           # Main file
  │   └── web.py            
  └── pyproject.toml        # Dependencies and Ruff
  └── uv.lock               # Dependencies versions

frontend/
  ├── src/
  │   ├── pages/            # Route pages
  │   ├── components/       # React components
  │   ├── hooks/            # Custom hooks
  │   └── lib/              # Utilities
  └── package.json
```

**Key Files**: `app/main.py` (FastAPI), `frontend/src/App.jsx` (React), `render.yaml` (deployment)

------------------------------------------------------------------------

## Troubleshooting

| Issue | Fix |
|-------|-----|
| MongoDB connection error | Check `MONGO_URI` and IP whitelist in Atlas |
| Clerk auth fails | Verify `CLERK_SECRET_KEY` and webhook URL |
| API not starting | Ensure MongoDB is running, check port 8000 |
| Login not working | Check `VITE_CLERK_PUBLISHABLE_KEY` and Clerk allowed origins |
| Video not displaying | Verify `STREAM_API_KEY` and browser permissions |
| Build fails | Delete `node_modules/` and reinstall: `npm install` |

------------------------------------------------------------------------

## License

This project is available for use. Please check with the repository owner for specific licensing information.