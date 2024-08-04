from src.services.criteria_service import CriteriaService
from fastapi import APIRouter
from src.schemas import CriteriaDTO

criteria_router = APIRouter(tags=["criteria"])

@criteria_router.get('/criteria/{interviwer_id}/{student_id}')
def get_criteria_of_participant(interviewer_id: str, student_id: str):
    return CriteriaService.get_criteria_of_participant(interviewer_id, student_id)

@criteria_router.get('/criteria/{interviewer_id}')
def get_criteria_by_interviewer(interviewer_id: str):
    return CriteriaService.get_criteria_by_interviewer(interviewer_id)

@criteria_router.get('/creteria')
def get_criteria_of_participant(interviewer_id: str, student_id: str):
    return CriteriaService.get_criteria_of_participant(interviewer_id, student_id)

@criteria_router.get('/criteria/average/{student_id}')
def get_avg_score(student_id: str):
    return CriteriaService.get_avg_score(student_id)
  
@criteria_router.get('/criterias')
def get_all():
    return CriteriaService.get_all()

@criteria_router.put('/criteria')
def update(criteria: CriteriaDTO) -> dict:
    return CriteriaService.update_criteria(criteria)
