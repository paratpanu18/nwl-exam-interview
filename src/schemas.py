from enum import Enum
from pydantic import BaseModel, Field

class SeniorType(str, Enum):
    PRIMARY = 'PRIMARY'
    SECONDARY = 'SECONDARY'
    ADMIN = 'ADMIN'

class CriteriaTypeDTO(BaseModel):
    name: str

class SeniorCreateDTO(BaseModel):
    name: str
    type: SeniorType

class JuniorCreateDTO(BaseModel):
    student_id: str
    name: str
    nickname: str
    academic_year: str

class CriteriaCreateDTO(BaseModel):
    interviewer_id: str
    student_id: str
    criteria_name: str
    score: int
    comment: str
    
class CriteriaDeleteDTO(BaseModel):
    interviewer_id: str 
    student_id: str
    criteria_name: str