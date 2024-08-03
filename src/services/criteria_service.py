from src.schemas import CriteriaDTO
from src.db import criteria_collection
from fastapi import HTTPException

class CriteriaService:
    def create(data: CriteriaDTO) -> dict:
        return
    
    def get_all() -> list[dict]:
        return 
    
    def delete(data: CriteriaDTO) -> dict:
        return
    
    @staticmethod
    def get_avg_score(student_id: str):
        for criteria in criteria_collection.find({'student_id': student_id}):
            pass
        return 
    
    @staticmethod
    def get_criteria_by_interviewer(interviewer_id: str):
        student_criteria_list = []
        for criteria in criteria_collection.find({'interviewer_id': interviewer_id}):
            # student_id = criteria['student_id']
            # student_criteria_list.append({
                
            # })
            pass

# [
#     {
#         'std_name': 'Fluk',
#         'criterias': [{
#             'criteria_name': 'Is this girl?',
#             'score': 8
#             },
#             {'criteria_name': 'Is he/she good?',
#             'score': 7
#             },
#         ]
#     },
# ]    