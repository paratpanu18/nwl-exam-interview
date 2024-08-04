from src.schemas import CriteriaDTO
from src.db import criteria_collection
from fastapi import HTTPException
from src.services.participant import ParticipantService

class CriteriaService:
    def create(data: CriteriaDTO) -> dict:
        criteria_collection.insert_one({
            'interviewer_id': data.interviewer_id,
            'student_id': data.student_id,
            'criteria_name': data.criteria_name,
            'score': data.score,
            'comment': data.comment,
        }).inserted_id
        return {'message': 'success'}
    
    def get_all() -> list[dict]:
        result = []
        for criteria in criteria_collection.find():
            result.append(criteria)
        return result
    
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
        student_id = None

        criteria_of_student = {}

        for criteria in criteria_collection.find({'interviewer_id': interviewer_id}):

            if student_id != criteria['student_id']:
                student_id = criteria['student_id']
                criteria_of_student = CriteriaService.get_criteria_of_participant(interviewer_id, student_id)
                student_criteria_list.append(criteria_of_student)

        return student_criteria_list
# [)
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
    def get_criteria_of_participant(interviewer_id: str, student_id: str):
        result = {}
        criterias_of_participant = []
        for criteria in criteria_collection.find({'interviewer_id': interviewer_id, 'student_id': student_id}):
            if not criterias_of_participant:
                result['student'] = ParticipantService.get_participant_by_student_id(student_id)
            criterias_of_participant.append({
                'criteria_name': criteria['criteria_name'],
                'score': str(criteria['score']),
                'comment': criteria['comment']
            })
        result['criterias'] = criterias_of_participant
        return result



