from fastapi import APIRouter
from fastapi_pagination import Page, paginate

from src.schemas import CriteriaTypeCreateDTO
from src.services.criteria_type import CriteriaTypeService

criteria_type_router = APIRouter(tags=["Criteria Type"])

class CriteriaTypeDTO(CriteriaTypeCreateDTO):
    id: str

@criteria_type_router.post('/criteriaType')
def create_new_criteria_type(criteria_type: CriteriaTypeCreateDTO) -> CriteriaTypeCreateDTO:
    return CriteriaTypeService.create_new_criteria_type(criteria_type)

@criteria_type_router.get('/criteriaType')
def get_all_criteria_types() -> Page[CriteriaTypeDTO]:
    return paginate(CriteriaTypeService.get_all_criteria_types())

@criteria_type_router.delete('/criteriaType/{criteria_type_id}')
def delete_criteria_type(criteria_type_id: str) -> None:
    return CriteriaTypeService.delete_criteria_type(criteria_type_id)

@criteria_type_router.put('/criteriaType/{criteria_type_id}')
def rename_criteria_type(criteria_type_id: str, new_name: str) -> CriteriaTypeCreateDTO:
    return CriteriaTypeService.rename_criteria_type(criteria_type_id, new_name)