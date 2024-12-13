from fastapi import APIRouter
from app.core.health.routes import router as core_health_router
from app.core.auth.routes import router as core_auth_router
from app.core.users.routes import router as core_users_router


api_router = APIRouter()

api_router.include_router(core_health_router)
api_router.include_router(core_auth_router)
api_router.include_router(core_users_router)
