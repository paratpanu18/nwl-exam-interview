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

@senior_router.delete("/senior/{name}")
def delete_senior_by_name(name: str) -> None:
    return SeniorService.delete_senior_by_name(name)