# Local Development Setup

## Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL (or use Docker)

## Quick Start

### 1. Clone and Setup

```bash
cd InterviewPrepMessenger

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# Frontend setup
cd ../frontend
npm install
cp .env.example .env.local
```

### 2. Configure Environment

#### Backend (.env)
```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/dailydev
SECRET_KEY=dev-secret-key-change-in-production
GROQ_API_KEY=gsk_your_key_here
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Database Setup

#### Option A: Local PostgreSQL
```bash
# Create database
createdb dailydev

# Run with asyncpg connection string
```

#### Option B: Docker
```bash
docker run --name dailydev-db \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=dailydev \
  -p 5432:5432 \
  -d postgres:15
```

#### Option C: Neon (Cloud - Free)
Use the Neon connection string in your .env

### 4. Seed Database

```bash
cd backend
source venv/bin/activate
python -m app.seed_data
```

### 5. Run Development Servers

Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Project Structure

```
InterviewPrepMessenger/
├── backend/
│   ├── app/
│   │   ├── api/routes/      # API endpoints
│   │   ├── core/            # Config, security, database
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   └── services/        # Business logic
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── app/                 # Next.js pages
│   ├── components/          # React components
│   ├── lib/                 # Utilities, API client, store
│   └── package.json
│
└── docs/
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - Register new user
- `POST /api/v1/auth/login` - Login and get token
- `GET /api/v1/auth/me` - Get current user

### Users
- `GET /api/v1/users/me` - Get profile
- `PATCH /api/v1/users/me` - Update profile
- `POST /api/v1/users/me/resume` - Upload resume
- `GET /api/v1/users/me/stats` - Get learning stats
- `POST /api/v1/users/me/whatsapp/connect` - Connect WhatsApp

### Topics
- `GET /api/v1/topics/` - List all topics
- `POST /api/v1/topics/select` - Select topics for learning
- `GET /api/v1/topics/me/selected` - Get user's selected topics

### Roadmap
- `GET /api/v1/roadmap/` - Get all roadmaps
- `GET /api/v1/roadmap/topic/{topic_id}` - Get roadmap for topic
- `GET /api/v1/roadmap/today` - Get today's concept

### Articles
- `GET /api/v1/articles/{id}` - Get article
- `POST /api/v1/articles/{id}/generate` - Generate article content
- `POST /api/v1/articles/{id}/save` - Save to library
- `DELETE /api/v1/articles/{id}/save` - Remove from library
- `GET /api/v1/articles/library/saved` - Get saved articles

### Webhooks
- `POST /api/v1/webhooks/whatsapp` - Twilio webhook

## Testing WhatsApp Locally

### Using ngrok
```bash
# Install ngrok
brew install ngrok  # or download from ngrok.com

# Expose local backend
ngrok http 8000

# Use ngrok URL as Twilio webhook
# https://xxxx.ngrok.io/api/v1/webhooks/whatsapp
```

### Manual Testing
1. Set up Twilio Sandbox
2. Configure webhook to your ngrok URL
3. Send "YES" from your WhatsApp to test

## Common Issues

### Import Errors
```bash
# Ensure you're in venv
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Database Connection Failed
- Check PostgreSQL is running
- Verify connection string format
- Ensure database exists

### CORS Errors
- Backend and frontend must be on specified ports
- Check FRONTEND_URL in backend .env

### LLM Errors
- Verify GROQ_API_KEY is set
- Check Groq API status
- Review rate limits (30 req/min free tier)

## Development Tips

### Adding New API Routes
1. Create route file in `backend/app/api/routes/`
2. Add schemas in `backend/app/schemas/`
3. Register in `backend/app/api/routes/__init__.py`

### Adding New Components
1. Create in `frontend/components/`
2. Use shadcn/ui patterns
3. Add to page as needed

### Database Changes
1. Modify model in `backend/app/models/`
2. Create migration (Alembic) or recreate tables
3. Update schemas if needed

## Code Quality

### Backend
```bash
# Format
black .
isort .

# Lint
flake8

# Type check
mypy app/
```

### Frontend
```bash
# Lint
npm run lint

# Type check
npx tsc --noEmit
```
