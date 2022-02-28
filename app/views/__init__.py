from app.views import auth, characters, comments, episodes, users
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(characters.router, prefix="/characters", tags=["characters"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(episodes.router, prefix="/episodes", tags=["episodes"])
api_router.include_router(users.router, prefix="/users", tags=["users"])