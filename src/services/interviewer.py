from fastapi import HTTPException
from src.schemas import InterviewerDTO
from src.db import interviewer_collection

TYPES = ['ADMIN', 'PRIMARY', 'SECONDARY']

class Interviewer:
    def __init__(self, name: str, type: str):
        self.name = name

        if type.upper() not in TYPES:
            raise HTTPException(status_code=400, detail="Invalid user type")

        self.type = type.upper()

    def save(self):
        result = interviewer_collection.insert_one({
            "name": self.name,
            "type": self.type
        }).inserted_id

        return {
            "id": str(result),
            "name": self.name,
            "type": self.type
        }

class InterviewerService:
    @staticmethod
    def create_interviewer(interviewerDTO: InterviewerDTO):

        if interviewer_collection.find_one({"name": interviewerDTO.name}):
            raise HTTPException(status_code=400, detail="Interviewer already exists")

        interviewer = Interviewer(
            name=interviewerDTO.name,
            type=interviewerDTO.type
        )

        interviewer.save()
        return interviewer

    @staticmethod
    def get_interviewers():
        interviewers = []
        for interviewer in interviewer_collection.find():
            interviewers.append({
                "id": str(interviewer["_id"]),
                "name": interviewer["name"],
                "type": interviewer["type"]
            })
        return interviewers
    
    @staticmethod
    def get_interviewer_by_name(name: str):
        interviewer = interviewer_collection.find_one({"name": name})
        if not interviewer:
            raise HTTPException(status_code=404, detail="Interviewer not found")
        return {
            "id": str(interviewer["_id"]),
            "name": interviewer["name"],
            "type": interviewer["type"]
        }
    
    @staticmethod
    def delete_interviewer_by_name(name: str):
        interviewer = interviewer_collection.find_one({"name": name})
        if not interviewer:
            raise HTTPException(status_code=404, detail="Interviewer not found")
        interviewer_collection.delete_one({"name": name})
        return {
            "message": "Interviewer deleted"
        }
        