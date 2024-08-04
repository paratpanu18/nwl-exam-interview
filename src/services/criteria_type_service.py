from src.schemas import CriteriaTypeDTO
from src.db import criteria_type_collection
from fastapi import HTTPException

class CriteriaTypeService:
    def create(data: CriteriaTypeDTO) -> dict:
        name = data.name
        criteria_type_collection.insert_one({
            'name': name
        })
        return {'name': name}
    
    def get_all() -> list[dict]:
        all_criteria_types = []
        for criteria_type in criteria_type_collection.find():
            all_criteria_types.append({
                'id': str(criteria_type['_id']),
                'name': criteria_type['name']
            })
        return all_criteria_types
    
    def delete(data: CriteriaTypeDTO) -> dict:
        name = data.name
        if not criteria_type_collection.find_one({'name': name}):
            raise HTTPException(status_code=404, detail="Criteria type not found")
        criteria_type_collection.delete_one({'name': name})
        return {'message': 'Deleted Successful'}
    
    def isCreteriaTypeValid(criteria_type_name: str):
        all_name = [criteria['name'] for criteria in criteria_type_collection.find()]
        return criteria_type_name in all_name