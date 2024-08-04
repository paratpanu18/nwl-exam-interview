from fastapi import APIRouter
from src.routers.junior import junior_router

api_router = APIRouter()
api_router.include_router(junior_router)