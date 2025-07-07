from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from db_schema import ToDOModel, ToDOCreateModel, ToDOUpdateModel
from ops import get_all, create, delete, update
from db import collection
from bson import ObjectId
from ops import get_completed, get_pending

todo_app = FastAPI()

@todo_app.get("/", response_model=List[ToDOModel])
def get_todo() -> List[ToDOModel]:
    return get_all()


@todo_app.post("/post", response_model=ToDOModel)
def post_todo(todo: ToDOCreateModel):
    try:
        created_todo = create(todo.model_dump())
        return created_todo
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@todo_app.put("/put", response_model=ToDOModel)
def put_todo(todo: ToDOUpdateModel):
    try:
        updated = update(todo.model_dump(by_alias=True))
        if not updated.get("updated"):
            raise HTTPException(status_code=404, detail="Todo not found")
        
        updated_doc = collection.find_one({"_id": ObjectId(todo.id)})
        updated_doc["_id"] = str(updated_doc["_id"])
        return ToDOModel(**updated_doc)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@todo_app.delete("/delete")
def delete_todo(todo: ToDOModel):
    try:
        result = delete(todo.model_dump(by_alias=True))
        if not result.get("deleted"):
            raise HTTPException(status_code=404, detail="Todo not found")
        return JSONResponse(content={"message": "Todo deleted successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@todo_app.get("/completed", response_model=List[ToDOModel])
def get_completed_todos() -> List[ToDOModel]:
    try:
        completed_todos = get_completed()
        if not completed_todos:
            raise HTTPException(status_code=404, detail="No completed todos found")
        return completed_todos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@todo_app.get("/pending", response_model=List[ToDOModel])
def get_pending_todos() -> List[ToDOModel]:
    try:
        pending_todos = get_pending()
        if not pending_todos:
            raise HTTPException(status_code=404, detail="No pending todos found")
        return pending_todos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


