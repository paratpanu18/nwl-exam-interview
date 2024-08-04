from src.schemas import CriteriaDTO
from src.db import criteria_collection
from fastapi import HTTPException
from src.services.participant import ParticipantService
from src.services.criteria_type_service import CriteriaTypeService
from src.services.interviewer import InterviewerService

class CriteriaService:
    def create(data: CriteriaDTO) -> dict:
        name = data.criteria_name

        if not CriteriaTypeService.isCriteriaTypeValid(name):
            return {'message': 'criteria not in type'}
        if data.interviewer_id not in [interviewer['id'] for interviewer in InterviewerService.get_interviewers()]:
            return {'message': 'Interview does not exist'}
        
        result = criteria_collection.insert_one({
            'interviewer_id': data.interviewer_id,
            'student_id': data.student_id,
            'criteria_name': name,
            'score': data.score,
            'comment': data.comment,
        }).inserted_id

        return {'criteria_id': result}
    
    def get_all() -> list[dict]:
        result = []
        for criteria in criteria_collection.find():
            result.append({
                'id': str(criteria['_id']),
                'criteria_name': criteria['criteria_name'],
                'interviewer_id': criteria['interviewer_id'],
                'student_id': criteria['student_id'],
                

            })
        return result
    
    def delete(data: CriteriaDTO) -> dict:
        return
    
    def update_criteria(data: CriteriaDTO) -> dict:
        if criteria_collection.find_one_and_update({
            'interviewer_id': data.interviewer_id,
            'student_id': data.student_id,
            'criteria_name': data.criteria_name,
        },
        {'$set':{
            'score': data.score,
            'comment': data.comment,
        }}
        ):
            return {'message': 'updated successful'}
        else:
            return CriteriaService.create(data)


    @staticmethod
    def get_avg_score(student_id: str):
        # for criteria in criteria_collection.find({'student_id': student_id}):
        #     pass
        return 
    
    @staticmethod
    def get_criteria_by_interviewer(interviewer_id: str):
        student_criteria_list = []
        student_id = None

        criteria_of_student = {}

        for criteria in criteria_collection.find({'interviewer_id': interviewer_id}):
            student_id = criteria['student_id']
            criteria_of_student = CriteriaService.get_criteria_of_participant(interviewer_id, student_id)
            student_id_list = [criteria['student']['student_id'] for criteria in student_criteria_list]
            if student_id in student_id_list:
                pass
            else:
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



