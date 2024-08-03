from pydantic import BaseModel

class InterviewerDTO(BaseModel):
    name: str
    type: str