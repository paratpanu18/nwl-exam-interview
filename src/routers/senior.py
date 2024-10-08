from fastapi import APIRouter
from fastapi_pagination import Page, paginate

from src.schemas import SeniorCreateDTO, SeniorType
from src.services.senior import SeniorService

senior_router = APIRouter(tags=["Senior"])

class SeniorDTO(SeniorCreateDTO):
    id: str

@senior_router.post("/senior")
def create_new_senior(senior: SeniorCreateDTO) -> SeniorDTO:
    return SeniorService.create_new_senior(senior)

@senior_router.get("/seniors")
def list_senior(type: SeniorType | None = None) -> Page[SeniorDTO]:
    return paginate(SeniorService.get_all_senior(type))

@senior_router.get("/senior/{name}")
def get_senior_by_name(name: str) -> SeniorDTO:
    return SeniorService.get_senior_by_name(name)

@senior_router.delete("/senior/{senior_id}")
def delete_senior_by_id(senior_id: str) -> None:
    return SeniorService.delete_senior_by_id(senior_id)

@senior_router.get("/senior/get_assigned_score/{senior_id}")
def get_assigned_score(senior_id: str):
    return SeniorService.get_assigned_score_by_senior(senior_id)

@senior_router.get("/senior/get_assigned_score/{senior_id}/{junior_id}")
def get_assigned_score(senior_id: str, junior_id: str):
    return SeniorService.get_assigned_score(senior_id, junior_id)

@senior_router.put("/senior/{senior_id}/")
def update_senior(senior_id: str, senior: SeniorCreateDTO):
    return SeniorService.update_senior(senior_id, senior)