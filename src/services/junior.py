from fastapi import HTTPException

from src.util import is_valid_student_id
from src.schemas import JuniorCreateDTO
from src.db import junior_collection

class JuniorService:
    @staticmethod
    def create_new_junior(junior: JuniorCreateDTO) -> dict:
        if junior_collection.find_one({"student_id": junior.student_id}):
            raise HTTPException(status_code=400, detail="Junior (Interviewee) already exists, student id must be unique for each interviewee")

        if not is_valid_student_id(junior.student_id):
            raise HTTPException(status_code=400, detail="Invalid student id format, student id must be in the format of '6x01xxxx'")

        if not junior.academic_year in ["1", "2", "3", "4"]:
            raise HTTPException(status_code=400, detail="Invalid academic year, academic year must be in the range of 1-4")

        result = junior_collection.insert_one({
            "student_id": junior.student_id,
            "name": junior.name,
            "nickname": junior.nickname.capitalize(),
            "academic_year": junior.academic_year
        })

        return {
            "id": str(result.inserted_id),
            "student_id": junior.student_id,
            "name": junior.name,
            "nickname": junior.nickname.capitalize(),
            "academic_year": junior.academic_year
        }
    
    @staticmethod
    def list_all_junior() -> list[dict]:
        result = []
        for junior in junior_collection.find():
            result.append({
                "id": str(junior["_id"]),
                "student_id": junior["student_id"],
                "name": junior["name"],
                "nickname": junior["nickname"],
                "academic_year": junior["academic_year"]
            })
        return result
    
    @staticmethod
    def get_junior_by_student_id(student_id: str) -> dict:
        if not is_valid_student_id(student_id):
            raise HTTPException(status_code=400, detail="Invalid student id format, student id must be in the format of '6x01xxxx'")
        
        target_junior = junior_collection.find_one({"student_id": student_id})
        if not target_junior:
            raise HTTPException(status_code=404, detail="Junior (Interviewee) not found")
        
        return {
            "id": str(target_junior["_id"]),
            "student_id": target_junior["student_id"],
            "name": target_junior["name"],
            "nickname": target_junior["nickname"],
            "academic_year": target_junior["academic_year"]
        }
    
    @staticmethod
    def delete_junior_by_student_id(student_id: str) -> dict:
        if not is_valid_student_id(student_id):
            raise HTTPException(status_code=400, detail="Invalid student id format, student id must be in the format of '6x01xxxx'")
        
        target_junior = junior_collection.find_one({"student_id": student_id})
        if not target_junior:
            raise HTTPException(status_code=404, detail="Junior (Interviewee) not found")
        
        junior_collection.delete_one({"student_id": student_id})

        return 
    
    @staticmethod
    def update_junior_by_student_id(student_id: str, data: JuniorCreateDTO) -> dict:
        if not is_valid_student_id(student_id):
            raise HTTPException(status_code=400, detail="Invalid student id format, student id must be in the format of '6x01xxxx'")

        target_junior = junior_collection.find_one({"student_id": student_id})
        if not target_junior:
            raise HTTPException(status_code=404, detail="Junior (Interviewee) not found")
        
        junior_collection.update_one({"student_id": student_id}, {"$set": data.dict()})
        
        return {
            "id": str(target_junior["_id"]),
            "student_id": data.student_id,
            "name": data.name,
            "nickname": data.nickname,
            "academic_year": data.academic_year   
        }