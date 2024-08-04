from src.schemas import CriteriaDTO
from src.db import criteria_collection, interviewer_collection
from fastapi import HTTPException
from bson.objectid import ObjectId
from src.services.participant import ParticipantService
from src.services.criteria_type_service import CriteriaTypeService

class CriteriaService:
    def create(data: CriteriaDTO) -> dict:
        name = data.criteria_name
        if not CriteriaTypeService.isCreteriaTypeValid(name):
            return {'message': 'criteria not in type'}
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
        
        total_score = {
            "student_id": student_id,
            "scores" : {}
        }
        
        for criteria in criteria_collection.find({'student_id': student_id}):
            criteria_type = criteria['criteria_name']
            interviewer_id = criteria['interviewer_id']
            interviewer_type = interviewer_collection.find_one({'_id': ObjectId(interviewer_id)})['type']

            if criteria_type not in total_score['scores']:
                total_score['scores'][criteria_type] = {
                    'primary_sum': 0,
                    'primary_count': 0,
                    'secondary_sum': 0,
                    'secondary_count': 0,
                    'total': 0
                }
            
            if interviewer_type == 'PRIMARY':
                total_score['scores'][criteria_type]['primary_sum'] += criteria['score']
                total_score['scores'][criteria_type]['primary_count'] += 1
            elif interviewer_type == 'SECONDARY':
                total_score['scores'][criteria_type]['secondary_sum'] += criteria['score']
                total_score['scores'][criteria_type]['secondary_count'] += 1

        for criteria_type in total_score['scores']:
            primary_sum = total_score['scores'][criteria_type]['primary_sum']
            primary_count = total_score['scores'][criteria_type]['primary_count']
            secondary_sum = total_score['scores'][criteria_type]['secondary_sum']
            secondary_count = total_score['scores'][criteria_type]['secondary_count']
            if secondary_count == 0 and primary_count == 0:
                total_score['scores'][criteria_type]['total'] = 0
                continue

            secondary_avg = secondary_sum / secondary_count if secondary_count != 0 else 0

            total_score['scores'][criteria_type]['total'] = (primary_sum + secondary_avg) / (primary_count + (1 if secondary_count != 0 else 0))

        return total_score
    
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



