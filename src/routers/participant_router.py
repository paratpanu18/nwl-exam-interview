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

@participant_router.delete("/participant/{student_id}")
def delete_participant_by_student_id(student_id: str):
    return ParticipantService.delete_participant_by_student_id(student_id)

@participant_router.put("/participant/{student_id}")
def update_participant_by_student_id(student_id: str, participant: ParticipantCreateDTO):
    return ParticipantService.update_participant_by_student_id(student_id, participant)