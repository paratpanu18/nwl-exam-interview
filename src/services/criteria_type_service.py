from src.schemas import CriteriaTypeDTO
from src.db import criteria_type_collection

class CriteriaTypeService:
    def create(data: CriteriaTypeDTO) -> dict:
        name = data.name
        criteria_type_collection.insert_one({
            'name': name
        })
        return {'name': name}
    
    def get_all() ->dict:
        all_criteria_types = []
        for criteria_type in criteria_type_collection.find():
            all_criteria_types.append({
                'id': str(criteria_type['_id']),
                'name': criteria_type['name']
            })
        return all_criteria_types