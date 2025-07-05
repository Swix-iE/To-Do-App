from db import collection
from db_schema import ToDOModel
from bson import ObjectId
from datetime import datetime, timezone


def update(data: dict):
    todo_id = data.get("_id")
    print("🛠️ Received _id:", todo_id)

    

    update_data = {k: v for k, v in data.items() if k != "_id"}
    update_data["updated_date"] = datetime.now(timezone.utc)

    result = collection.update_one(
        {"_id": todo_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        return {"error": "No document found with that _id"}

    return {"updated": result.modified_count > 0}
