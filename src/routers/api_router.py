from fastapi import APIRouter
from src.routers.junior import junior_router
from src.routers.senior import senior_router
from src.routers.criteria_type import criteria_type_router

api_router = APIRouter()
api_router.include_router(junior_router)
api_router.include_router(senior_router)
api_router.include_router(criteria_type_router)