from fastapi import HTTPException
from bson.objectid import ObjectId

from src.schemas import CriteriaTypeCreateDTO
from src.db import criteria_type_collection

class CriteriaTypeService:
    def create_new_criteria_type(data: CriteriaTypeCreateDTO) -> dict:
        name = data.name
        if not CriteriaTypeService.isCriteriaTypeValid(name):
            raise HTTPException(status_code=400, detail=f"This criteria type already exists: {name}")

        result = criteria_type_collection.insert_one({
            'name': name
        })

        return {
            'id': str(result.inserted_id),
            'name': name
        }  
      
    def get_all_criteria_types() -> list[dict]:
        all_criteria_types = []
        for criteria_type in criteria_type_collection.find():
            all_criteria_types.append({
                'id': str(criteria_type['_id']),
                'name': criteria_type['name']
            })
        return all_criteria_types
    
    def delete_criteria_type(data: CriteriaTypeCreateDTO) -> None:
        name = data.name
        if not criteria_type_collection.find_one({'name': name}):
            raise HTTPException(status_code=404, detail="Criteria type not found")
        
        criteria_type_collection.delete_one({'name': name})
        return
    
    def rename_criteria_type(criteria_type_id: str, new_name: str) -> CriteriaTypeCreateDTO:
        target_criteria_type = criteria_type_collection.find_one({"_id": ObjectId(criteria_type_id)})
        if not target_criteria_type:
            raise HTTPException(status_code=404, detail="Criteria type not found")
        
        if not CriteriaTypeService.isCriteriaTypeValid(new_name):
            raise HTTPException(status_code=400, detail=f"This criteria type already exists: {new_name}")
        
        criteria_type_collection.update_one({"_id": ObjectId(criteria_type_id)}, {"$set": {"name": new_name}})
        return {
            'id': criteria_type_id,
            'name': new_name
        }
    
    def isCriteriaTypeValid(criteria_type_name: str) -> bool:
        existing_criteria_type_name = [criteria['name'] for criteria in criteria_type_collection.find()]
        return criteria_type_name not in existing_criteria_type_name