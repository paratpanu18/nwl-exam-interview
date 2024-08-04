from fastapi import HTTPException
from src.schemas import SeniorCreateDTO
from src.db import senior_collection

TYPES = ['ADMIN', 'PRIMARY', 'SECONDARY']

class SeniorService:
    @staticmethod
    def create_new_senior(senior: SeniorCreateDTO):
        name = senior.name
        type = senior.type

        if type not in TYPES:
            raise HTTPException(status_code=400, detail="Invalid senior (Interviewer) type: [ADMIN, PRIMARY, SECONDARY]")
        
        if senior_collection.find_one({"name": name}):
            raise HTTPException(status_code=400, detail="Senior (Interviewer) already exists, name must be unique for each interviewer")
        
        result = senior_collection.insert_one({
            "name": name,
            "type": type
        }).inserted_id

        return {
            "id": str(result),
            "name": name,
            "type": type
        }

    @staticmethod
    def get_all_senior(type: str | None = None):
        seniors = []
        query = {} if not type else {"type": type}
        for senior in senior_collection.find(query):
            seniors.append({
                "id": str(senior["_id"]),
                "name": senior["name"],
                "type": senior["type"]
            })
        return seniors
        
    @staticmethod
    def get_senior_by_name(name: str):
        target_senior = senior_collection.find_one({"name": name})
        if not target_senior:
            raise HTTPException(status_code=404, detail="Senior (Interviewer) not found")
        
        return {
            "id": str(target_senior["_id"]),
            "name": target_senior["name"],
            "type": target_senior["type"]
        }
    
    @staticmethod
    def delete_senior_by_name(name: str):
        target_senior = senior_collection.find_one({"name": name})
        if not target_senior:
            raise HTTPException(status_code=404, detail="Senior (Interviewer) not found")
        
        senior_collection.delete_one({"name": name})
        return
        