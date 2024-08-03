from fastapi import APIRouter

from src.services.participant import ParticipantService
from src.schemas import ParticipantCreateDTO

participant_router = APIRouter(tags=["participant"])

@participant_router.post("/participant")
def create_participant(participant: ParticipantCreateDTO):
    return ParticipantService.create_participant(participant)

@participant_router.get("/participants")
def get_participants():
    return ParticipantService.get_all_participants()

@participant_router.get("/participant/{student_id}")
def get_participant_by_student_id(student_id: str):
    return ParticipantService.get_participant_by_student_id(student_id)