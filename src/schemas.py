from pydantic import BaseModel

class CriteriaTypeDTO(BaseModel):
    name: str
    
class InterviewerDTO(BaseModel):
    name: str
    type: str
