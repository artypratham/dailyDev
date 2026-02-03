# DailyDev - Free Daily Interview Prep Platform

Transform interview preparation into a daily habit through bite-sized, real-world problem-driven learning delivered via WhatsApp.

## 🎯 The Problem

Software engineers working full-time cannot dedicate 8+ hours daily for interview prep. They need:
- Consistent daily learning (not overwhelming)
- Real-world context (not dry theory)
- Zero friction (WhatsApp, not another app)
- Completely FREE access

## 💡 The Solution

A system that sends ONE engaging hook message daily via WhatsApp, explaining a real-world engineering problem, then delivers expert-level content when the user wants to learn more.

## 🏗️ Architecture

```
Frontend (Next.js 14)  →  Backend (FastAPI)  →  Services
     │                         │                   │
     │                         │                   ├── Groq API (LLM)
     │                         │                   ├── Twilio (WhatsApp)
     │                         │                   └── Neon (PostgreSQL)
     │                         │
     └─────── Vercel ──────────┴────── Railway ──────────
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL (or use Neon free tier)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with your credentials
npm run dev
```

## 📁 Project Structure

```
/
├── backend/                 # FastAPI Python backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Config, security, dependencies
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── migrations/         # Alembic migrations
│   └── tests/              # Pytest tests
│
├── frontend/               # Next.js 14 frontend
│   ├── app/               # App router pages
│   ├── components/        # React components
│   └── lib/               # Utilities
│
└── docs/                  # Documentation
```

## 🔑 Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://...
GROQ_API_KEY=gsk_...
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_NUMBER=+14155238886
SECRET_KEY=your-secret-key
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📚 Topics Covered

- ✅ Data Structures & Algorithms (DSA)
- ✅ System Design (HLD)
- ✅ Low-Level Design (LLD)
- ✅ Applied AI/ML Engineering
- ✅ Computer Networks
- ✅ Operating Systems
- ✅ Database Management Systems
- ✅ Backend Engineering
- ✅ Scalability & Performance
- ✅ Distributed Systems

## 🎮 Features

- **Resume Analysis**: Upload your resume for personalized learning paths
- **Daily WhatsApp Hooks**: Engaging real-world problems delivered daily
- **Expert Articles**: ELI5 + Technical deep dives + Code implementations
- **Progress Tracking**: Streaks, badges, and analytics
- **Mobile-First**: Beautiful, responsive article viewer

## 🛠️ Tech Stack

**Frontend:**
- Next.js 14 (App Router)
- TypeScript
- TailwindCSS + shadcn/ui
- React Query

**Backend:**
- FastAPI (Python 3.11+)
- SQLAlchemy + Alembic
- Groq API (Llama 3.1 70B)
- Twilio WhatsApp API

**Infrastructure:**
- Vercel (Frontend)
- Railway (Backend)
- Neon (PostgreSQL)
- Upstash (Redis)

## 👤 Author

**Prathamesh Dharmadhikari**
- Software Engineer
- Specializing in AI/ML, Full-Stack Development
