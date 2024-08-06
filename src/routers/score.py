from fastapi import APIRouter

from src.services.score import ScoreService
from src.services.junior import JuniorService
from src.schemas import ScoreCreateDTO

score_router = APIRouter(tags=["Score"])

@score_router.post('/score')
def assign_score_to_junior(score: ScoreCreateDTO) -> dict:
    return ScoreService.assign_score_to_junior(score)

@score_router.put('/score')
def update_score(score: ScoreCreateDTO) -> dict:
    return ScoreService.update_score(score)