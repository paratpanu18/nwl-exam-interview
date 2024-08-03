from fastapi import HTTPException

from src.schemas import ParticipantCreateDTO
from src.db import participant_collection

class Participant:
    def __init__(self, student_id: str, name: str, nickname: str, academic_year: str):
        self.student_id = student_id
        self.name = name
        self.nickname = nickname
        self.academic_year = academic_year
    
    def save(self):
        result = participant_collection.insert_one({
            "student_id": self.student_id,
            "name": self.name,
            "nickname": self.nickname,
            "academic_year": self.academic_year
        }).inserted_id

        return {
            "id": str(result),
            "student_id": self.student_id,
            "name": self.name,
            "nickname": self.nickname,
            "academic_year": self.academic_year
        }
        

class ParticipantService:
    def create_participant(data: ParticipantCreateDTO):
        if participant_collection.find_one({"student_id": data.student_id}):
            raise HTTPException(status_code=400, detail="Participant already exists")

        participant = Participant(
            student_id=data.student_id,
            name=data.name,
            nickname=data.nickname,
            academic_year=data.academic_year
        )

        participant.save()
        return participant
    
    def get_all_participants():
        participants = []
        for participant in participant_collection.find():
            participants.append({
                "id": str(participant["_id"]),
                "student_id": participant["student_id"],
                "name": participant["name"],
                "nickname": participant["nickname"],
                "academic_year": participant["academic_year"]
            })
        return participants
    
    def get_participant_by_student_id(student_id: str):
        participant = participant_collection.find_one({"student_id": student_id})
        if not participant:
            raise HTTPException(status_code=404, detail="Participant not found")
        return {
            "id": str(participant["_id"]),
            "student_id": participant["student_id"],
            "name": participant["name"],
            "nickname": participant["nickname"],
            "academic_year": participant["academic_year"]
        }