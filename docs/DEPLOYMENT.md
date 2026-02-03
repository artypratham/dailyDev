# Deployment Guide

## Prerequisites

Before deploying, ensure you have accounts on:
- [Vercel](https://vercel.com) - Frontend hosting
- [Railway](https://railway.app) - Backend hosting
- [Neon](https://neon.tech) - PostgreSQL database
- [Groq](https://console.groq.com) - LLM API (free)
- [Twilio](https://twilio.com) - WhatsApp messaging

## Environment Variables

### Backend (Railway)

```
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dailydev
SECRET_KEY=your-super-secret-key-minimum-32-chars
GROQ_API_KEY=gsk_your_groq_api_key
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=+14155238886
FRONTEND_URL=https://your-app.vercel.app
ENVIRONMENT=production
```

### Frontend (Vercel)

```
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

## Step-by-Step Deployment

### 1. Database Setup (Neon)

1. Go to [Neon Console](https://console.neon.tech)
2. Create a new project
3. Copy the connection string
4. Note: Neon provides free PostgreSQL with 10GB storage

### 2. Get API Keys

#### Groq API
1. Go to [Groq Console](https://console.groq.com)
2. Create an API key
3. Free tier includes Llama 3.1 70B

#### Twilio WhatsApp
1. Sign up at [Twilio](https://twilio.com)
2. Go to Console > Messaging > Try WhatsApp
3. Follow sandbox setup instructions
4. Note your Account SID and Auth Token

### 3. Deploy Backend (Railway)

1. Go to [Railway](https://railway.app)
2. Create new project > Deploy from GitHub
3. Select the `backend` folder
4. Add environment variables
5. Railway will auto-detect Dockerfile and deploy

### 4. Deploy Frontend (Vercel)

1. Go to [Vercel](https://vercel.com)
2. Import Git Repository
3. Set root directory to `frontend`
4. Add environment variable: `NEXT_PUBLIC_API_URL`
5. Deploy

### 5. Configure Twilio Webhook

1. Go to Twilio Console
2. Navigate to Messaging > Settings > WhatsApp Sandbox Settings
3. Set webhook URL: `https://your-backend.railway.app/api/v1/webhooks/whatsapp`
4. Set HTTP POST

### 6. Seed Database

After backend deployment, seed initial topics:

```bash
# Connect to Railway shell or run locally with production DB
python -m app.seed_data
```

## Verification Checklist

- [ ] Frontend loads at Vercel URL
- [ ] Backend health check: `GET /health` returns `{"status": "healthy"}`
- [ ] User can sign up and login
- [ ] Topics load on onboarding page
- [ ] WhatsApp test message sends successfully
- [ ] Article generation works

## Troubleshooting

### CORS Issues
- Ensure `FRONTEND_URL` is set correctly in backend
- Check that the URL doesn't have a trailing slash

### Database Connection
- Verify DATABASE_URL format includes `+asyncpg`
- Check Neon dashboard for connection limits

### WhatsApp Not Working
- Verify Twilio credentials
- Check webhook URL is accessible
- Ensure phone number format includes country code

### LLM Generation Slow
- Groq is typically fast, but check API status
- Increase timeout in client settings if needed

## Monitoring

### Backend Logs
- Railway: View in project dashboard
- Add Sentry for error tracking (optional)

### Frontend Analytics
- Vercel Analytics (built-in)
- Add PostHog or Plausible for detailed analytics

## Scaling

### When to Scale
- Backend: >100 concurrent users
- Database: >1GB data or >100 connections

### How to Scale
- Railway: Increase replicas in settings
- Neon: Upgrade to paid tier for more resources
- Consider adding Redis cache (Upstash) for frequent queries
