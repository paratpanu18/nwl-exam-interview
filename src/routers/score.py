from fastapi import APIRouter

from src.services.score import ScoreService
from src.schemas import ScoreCreateDTO, ManyScoreCreateDTO

score_router = APIRouter(tags=["Score"])

@score_router.post('/score')
def assign_score_to_junior(score: ScoreCreateDTO) -> dict:
    return ScoreService.assign_score_to_junior(score)

@score_router.put('/score')
def update_score(score: ScoreCreateDTO) -> dict:
    return ScoreService.update_score(score)

@score_router.post('/many_score')
def assign_scores_to_junior(score: ManyScoreCreateDTO) -> dict:
    return ScoreService.assign_scores_to_junior(score)

@score_router.put('/many_scores')
def update_scores(score: ManyScoreCreateDTO) -> dict:
    return ScoreService.update_scores(score)