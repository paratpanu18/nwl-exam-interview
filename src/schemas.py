from pydantic import BaseModel, Field

class CriteriaTypeDTO(BaseModel):
    name: str
    
class InterviewerDTO(BaseModel):
    name: str
    type: str

class CriteriaCreateDTO(BaseModel):
    interviewer_id: str
    student_id: str
    criteria_name: str
    score: int
    comment: str
    
class CriteriaDeleteDTO(BaseModel):
    interviewer_id: str | None = None
    student_id: str | None = None
    criteria_name: str | None = None

class ParticipantCreateDTO(BaseModel):
    student_id: str
    name: str
    nickname: str
    academic_year: str


