from fastapi import HTTPException
from bson.objectid import ObjectId

from src.schemas import SeniorCreateDTO
from src.db import senior_collection, score_collection, junior_collection, criteria_type_collection

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
        score_collection.delete_many({"senior_id": str(target_senior["_id"])})
        return
    
    @staticmethod
    def get_assigned_score(senior_id: str, junior_id: str):
        senior = senior_collection.find_one({"_id": ObjectId(senior_id)})
        if not senior:
            raise HTTPException(status_code=404, detail="Senior not found")
        
        junior = junior_collection.find_one({"_id": ObjectId(junior_id)})
        if not junior:
            raise HTTPException(status_code=404, detail="Junior not found")

        result = {
            "senior_id": senior_id,
            "senior_name": senior["name"],
            "junior_id": junior_id,
            "junior_name": junior["name"],
            "scores": [

            ]
        }

        for score in score_collection.find({"senior_id": senior_id, "junior_id": junior_id}):
            criteria_id = score["criteria_id"]
            criteria_name = criteria_type_collection.find_one({"_id": ObjectId(criteria_id)})["name"]

            result["scores"].append({
                "criteria_id": criteria_id,
                "criteria_name": criteria_name,
                "score": score["score"],
                "comment": score["comment"]
            })
        
        return result
    
    @staticmethod
    def get_assigned_score_by_senior(senior_id: str):

        senior = senior_collection.find_one({"_id": ObjectId(senior_id)})
        if not senior:
            raise HTTPException(status_code=404, detail="Senior not found")

        result = {
            "senior_id": senior_id,
            "senior_name": senior["name"],
            "juniors": [

            ],
        }

        added_junior_ids = []

        for score in score_collection.find({"senior_id": senior_id}):

            junior_id = score["junior_id"]

            if junior_id not in added_junior_ids:

                junior = junior_collection.find_one({"_id": ObjectId(junior_id)})

                added_junior_ids.append(junior_id)

                sub_result = {
                    "junior_id": junior_id,
                    "junior_name": junior["name"],
                    "scores": [


                    ]
                }

                result["juniors"].append(sub_result)
            
            index = added_junior_ids.index(junior_id)

            junior = result["juniors"][index]

            criteria_id = score["criteria_id"]
            criteria_name = criteria_type_collection.find_one({"_id": ObjectId(criteria_id)})["name"]

            junior["scores"].append({
                "criteria_id": criteria_id,
                "criteria_name": criteria_name,
                "score": score["score"],
                "comment": score["comment"]
                }
            )
        

        for junior in junior_collection.find():

            result["juniors"].append({
                "junior_id": str(junior["_id"]),
                "junior_name": junior["name"],
                "scores": []
            })


        for criteria in criteria_type_collection.find():
            
            criteria_id = str(criteria["_id"])

            for junior in result["juniors"]:

                if criteria_id not in [score["criteria_id"] for score in junior["scores"]]:

                    junior["scores"].append({
                        "criteria_id": criteria_id,
                        "criteria_name": criteria["name"],
                        "score": 0,
                        "comment": ""
                    })

        return result
