from enum import Enum
from typing import Union
from pydantic import BaseModel

class SeniorType(str, Enum):
    PRIMARY = 'PRIMARY'
    SECONDARY = 'SECONDARY'
    ADMIN = 'ADMIN'

class CriteriaTypeCreateDTO(BaseModel):
    name: str

class SeniorCreateDTO(BaseModel):
    name: str
    type: SeniorType

class JuniorCreateDTO(BaseModel):
    student_id: str
    name: str
    nickname: str
    academic_year: str

class ScoreCreateDTO(BaseModel):
    junior_id: str
    senior_id: str
    criteria_id: str
    score: int
    comment: Union[str, None] = None

class ScoreSetDTO(BaseModel):
    criteria_id: str
    score: int
    comment: Union[str, None] = None

class ManyScoreCreateDTO(BaseModel):
    junior_id: str
    senior_id: str
    score_set: list[ScoreSetDTO]                                                                                                      