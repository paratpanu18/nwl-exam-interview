from fastapi import APIRouter
from src.schemas import InterviewerDTO
from src.services.interviewer import InterviewerService

interviewer_router = APIRouter(tags=["interviewer"])

@interviewer_router.post("/interviewer")
def create_interviewer(interviewerDTO: InterviewerDTO):
    return InterviewerService.create_interviewer(interviewerDTO)

@interviewer_router.get("/interviewers")
def get_interviewers():
    return InterviewerService.get_interviewers()

@interviewer_router.get("/interviewer/{name}")
def get_interviewer_by_name(name: str):
    return InterviewerService.get_interviewer_by_name(name)