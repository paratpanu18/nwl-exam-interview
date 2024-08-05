from fastapi import APIRouter
from fastapi_pagination import Page, paginate

from src.services.junior import JuniorService
from src.services.score import ScoreService
from src.schemas import JuniorCreateDTO

junior_router = APIRouter(tags=["Junior"])

class JuniorDTO(JuniorCreateDTO):
    id: str

@junior_router.get('/junior/score/{student_id}')
def get_average_score_by_student_id(student_id: str):
    junior: dict = JuniorService.get_junior_by_student_id(student_id)
    junior.update({"score": ScoreService.get_average_score_by_student_id(student_id)})
    total_avg_score = {"total_avg_score": sum(junior["score"].values()) / len(junior["score"])} if len(junior["score"]) > 0 else {"total_avg_score": 0}
    junior.update(total_avg_score)

    return junior

@junior_router.get('/junior/score')
def get_all_junior_score() -> Page[dict]:
    juniors = JuniorService.list_all_junior()
    for junior in juniors:
        junior.update({"score": ScoreService.get_average_score_by_student_id(junior["student_id"])})
        total_avg_score = {"total_avg_score": sum(junior["score"].values()) / len(junior["score"])} if len(junior["score"]) > 0 else {"total_avg_score": 0}
        junior.update(total_avg_score)

    return paginate(juniors)

@junior_router.post("/junior")
def create_new_junior(junior: JuniorCreateDTO) -> JuniorDTO:
    return JuniorService.create_new_junior(junior)

@junior_router.get("/junior/{student_id}")
def get_junior_by_student_id(student_id: str):
    return JuniorService.get_junior_by_student_id(student_id)

@junior_router.get("/juniors")
def list_junior() -> Page[JuniorDTO]:
    return paginate(JuniorService.list_all_junior())

@junior_router.delete("/junior/{student_id}")
def delete_junior_by_student_id(student_id: str) -> None:
    return JuniorService.delete_junior_by_student_id(student_id)

@junior_router.put("/junior/{student_id}")
def update_junior_by_student_id(student_id: str, new_data: JuniorCreateDTO) -> JuniorDTO:
    return JuniorService.update_junior_by_student_id(student_id, new_data)


