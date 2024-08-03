from src.services.criteria_type_service import CriteriaTypeService
from fastapi import APIRouter
from src.schemas import CriteriaTypeDTO

criteria_type_router = APIRouter(tags=["criteriaType"])

@criteria_type_router.post('/criteriaType')
def create(criteria_type: CriteriaTypeDTO) -> dict:
    return CriteriaTypeService.create(criteria_type)

@criteria_type_router.get('/criteriaType')
def get_all() -> list[dict]:
    return CriteriaTypeService.get_all()