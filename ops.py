from db import collection
from db_schema import ToDOModel
from bson import ObjectId
from datetime import datetime, timezone



def get_all():
    todos = []
    for col in collection.find():
        col["_id"] = str(col["_id"])
        todos.append(ToDOModel(**col))
    return todos

def create(data: dict):

    data["created_date"] = datetime.now(timezone.utc)
    data["updated_date"] = datetime.now(timezone.utc)

    res = collection.insert_one(data)
    col = collection.find_one({"_id": res.inserted_id})
    col["_id"] = str(col["_id"])
    return ToDOModel(**col)



def delete(data: dict):
    todo_id = data.get("_id")
    if not todo_id:
        return {"error": "Missing _id"}

    try:
        todo_id = ObjectId(todo_id)
    except Exception as e:
        return {"error": f"Invalid ObjectId: {e}"}

    result = collection.delete_one({"_id": todo_id})
    return {"deleted": result.deleted_count > 0}


def update(data: dict):
    todo_id = data.get("_id")
    if not todo_id:
        return {"error": "Missing _id"}

    try:
        todo_id = ObjectId(todo_id)
    except Exception as e:
        return {"error": f"Invalid ObjectId: {e}"}

    update_data = {k: v for k, v in data.items() if k != "_id"}
    update_data["updated_date"] = datetime.now(timezone.utc)

    result = collection.update_one(
        {"_id": todo_id},
        {"$set": update_data}
    )

    
    return {"updated": result.modified_count > 0}

