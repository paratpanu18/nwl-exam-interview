from src.schemas import CriteriaCreateDTO, CriteriaDeleteDTO
from src.db import criteria_collection, interviewer_collection
from fastapi import HTTPException, status
from services.junior import ParticipantService
from services.criteria_type import CriteriaTypeService
from services.senior import InterviewerService
from services.junior import ParticipantService
from bson.objectid import ObjectId

class CriteriaService:
    def create(data: CriteriaCreateDTO) -> dict:
        name = data.criteria_name
        student_id = data.student_id
        interviewer_id = data.interviewer_id

        if not CriteriaTypeService.isCriteriaTypeValid(name):
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Criteria name is not exist')
        if interviewer_id not in [interviewer['id'] for interviewer in InterviewerService.get_interviewers()]:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Interview id does not exist')
        if not ParticipantService.get_participant_by_student_id(student_id):
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Student id does not exist')

        result = criteria_collection.insert_one({
            'interviewer_id': interviewer_id,
            'student_id': student_id,
            'criteria_name': name,
            'score': data.score,
            'comment': data.comment,
        })

        return {'criteria_id': str(result.inserted_id)}
    

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
    

    def delete(data: CriteriaDeleteDTO) -> dict:
        interviewer_id = data.interviewer_id
        student_id = data.student_id
        criteria_name = data.criteria_name
        query = {}

        if interviewer_id: 
            query['interviewer_id'] = interviewer_id
            if interviewer_id not in [interviewer['id'] for interviewer in InterviewerService.get_interviewers()]:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Interview id does not exist')
        if student_id: 
            query['student_id'] = student_id
            if not ParticipantService.get_participant_by_student_id(student_id):
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Student id does not exist')
        if criteria_name: 
            query['criteria_name'] = criteria_name
            if not CriteriaTypeService.isCriteriaTypeValid(criteria_name):
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Criteria name is not exist')
        if query == {}:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Body does not have any field')
        
        d = criteria_collection.delete_many(query)

        return {'deleted_count': d.deleted_count}
    

    def update_criteria(data: CriteriaCreateDTO) -> dict:
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



