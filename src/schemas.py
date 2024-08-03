from pydantic import BaseModel

class CriteriaTypeDTO(BaseModel):
    name: str
    
class InterviewerDTO(BaseModel):
    name: str
    type: str

class ParticipantCreateDTO(BaseModel):
    student_id: str
    name: str
    nickname: str
    academic_year: str