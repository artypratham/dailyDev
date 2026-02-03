from fastapi import APIRouter
from app.api.routes import auth, users, topics, roadmap, articles, webhooks

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(topics.router, prefix="/topics", tags=["Topics"])
api_router.include_router(roadmap.router, prefix="/roadmap", tags=["Roadmap"])
api_router.include_router(articles.router, prefix="/articles", tags=["Articles"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
