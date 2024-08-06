from bson.objectid import ObjectId
from fastapi import HTTPException, status

from src.db import score_collection, junior_collection, senior_collection, criteria_type_collection
from src.schemas import ScoreCreateDTO

class ScoreService:
    def assign_score_to_junior(data: ScoreCreateDTO):
        junior = junior_collection.find_one({"_id": ObjectId(data.junior_id)})
        if not junior:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Junior not found")
        junior_name = junior["name"]

        senior = senior_collection.find_one({"_id": ObjectId(data.senior_id)})
        if not senior:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Senior not found")
        senior_name = senior["name"]

        criteria = criteria_type_collection.find_one({"_id": ObjectId(data.criteria_id)})
        if not criteria:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Criteria not found")
        criteria_name = criteria["name"]

        if score_collection.find_one({"junior_id": data.junior_id, "senior_id": data.senior_id, "criteria_id": data.criteria_id}):
            existing_score = score_collection.find_one({"junior_id": data.junior_id, "senior_id": data.senior_id, "criteria_id": data.criteria_id})
            detail_message = f"Score already exists for junior: {junior_name}, senior: {senior_name}, criteria: {criteria_name} -> score: {existing_score['score']}, comment: {existing_score['comment']}. Please use PUT method to update the score"
            
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail_message)

        result = score_collection.insert_one({
            "junior_id": data.junior_id,
            "senior_id": data.senior_id,
            "criteria_id": data.criteria_id,
            "score": data.score,
            "comment": data.comment if data.comment else ""
        }).inserted_id

        return {
            "id": str(result),
            "junior_id": junior_name,
            "senior_id": senior_name,
            "criteria_id": criteria_name,
            "score": data.score,
            "comment": data.comment if data.comment else ""
        }

    def get_average_score_by_student_id(student_id: str) -> dict:
        tmp = {}
        
        junior_id = str(junior_collection.find_one({"student_id": student_id})["_id"])
        for score in score_collection.find({"junior_id": junior_id}):
            criteria_id = score["criteria_id"]
            criteria_name = criteria_type_collection.find_one({"_id": ObjectId(criteria_id)})["name"]

            if criteria_name not in tmp:
                tmp[criteria_name] = {
                    "sum_of_primary_interviewer": 0,
                    "primary_interviewer_count": 0,
                    "sum_of_secondary_interviewer": 0,
                    "secondary_interviewer_count": 0,
                }

            interviewer_type = senior_collection.find_one({"_id": ObjectId(score["senior_id"])})["type"]
            if interviewer_type == "PRIMARY":
                tmp[criteria_name]["sum_of_primary_interviewer"] += score["score"]
                tmp[criteria_name]["primary_interviewer_count"] += 1
            else:
                tmp[criteria_name]["sum_of_secondary_interviewer"] += score["score"]
                tmp[criteria_name]["secondary_interviewer_count"] += 1

        result = {}
        for criteria_name in tmp:
            if tmp[criteria_name]["secondary_interviewer_count"] == 0 and tmp[criteria_name]["primary_interviewer_count"] == 0:
                result[criteria_name] = 0
                continue

            secondary_avg = tmp[criteria_name]["sum_of_secondary_interviewer"] / tmp[criteria_name]["secondary_interviewer_count"] if tmp[criteria_name]["secondary_interviewer_count"] != 0 else 0
            result[criteria_name] = (tmp[criteria_name]["sum_of_primary_interviewer"] + secondary_avg) / (tmp[criteria_name]["primary_interviewer_count"] + (1 if tmp[criteria_name]["secondary_interviewer_count"] != 0 else 0))

        return result

    def update_score(data: ScoreCreateDTO) -> dict:
        junior = junior_collection.find_one({"_id": ObjectId(data.junior_id)})
        if not junior:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Junior not found")
        junior_name = junior["name"]

        senior = senior_collection.find_one({"_id": ObjectId(data.senior_id)})
        if not senior:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Senior not found")
        senior_name = senior["name"]

        criteria = criteria_type_collection.find_one({"_id": ObjectId(data.criteria_id)})
        if not criteria:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Criteria not found")
        criteria_name = criteria["name"]

        if not score_collection.find_one({"junior_id": data.junior_id, "senior_id": data.senior_id, "criteria_id": data.criteria_id}):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Score not found")

        result = score_collection.update_one({
            "junior_id": data.junior_id,
            "senior_id": data.senior_id,
            "criteria_id": data.criteria_id
        }, {
            "$set": {
                "score": data.score,
                "comment": data.comment if data.comment else ""
            }
        })

        return {
            "junior_id": junior_name,
            "senior_id": senior_name,
            "criteria_id": criteria_name,
            "score": data.score,
            "comment": data.comment if data.comment else ""
        }

            

            