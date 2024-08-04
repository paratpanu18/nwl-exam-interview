from src.services.criteria_service import CriteriaService
from fastapi import APIRouter, Query
from src.schemas import CriteriaDTO

criteria_router = APIRouter(tags=["criteria"])

@criteria_router.post('/criteria')
def create(criteria: CriteriaDTO) -> dict:
    return CriteriaService.create(criteria)

# @criteria_router.get('/criteria/{student_id}') #for admin
# def get_avg_score(student_id: str):
#     return CriteriaService.get_avg_score(student_id)

@criteria_router.get('/criteria/')
def get_criteria_by_interviewer(interviewer_id: str):
    return CriteriaService.get_criteria_by_interviewer(interviewer_id)

@criteria_router.get('/creteria/')
def get_criteria_of_participant(interviewer_id: str, student_id: str):
    return CriteriaService.get_criteria_of_participant(interviewer_id, student_id)

@criteria_router.put('/criteria')
def update(criteria: CriteriaDTO) -> dict:
    return CriteriaService.update_criteria(criteria)