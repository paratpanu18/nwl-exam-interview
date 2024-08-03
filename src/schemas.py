from pydantic import BaseModel

class CriteriaTypeDTO(BaseModel):
    name: str
    
class InterviewerDTO(BaseModel):
    name: str
    type: str

class CriteriaDTO(BaseModel):
    interviewer_id: str
    student_id: str
    criteria_name: str
    score: int
    comment: str
    
class ParticipantCreateDTO(BaseModel):
    student_id: str
    name: str
    nickname: str
    academic_year: str
