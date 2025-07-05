from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from db_schema import ToDOModel
from ops import get_all, create, delete, update

todo_app = FastAPI()

@todo_app.get("/", response_model=List[ToDOModel])
def get_todo() -> List[ToDOModel]:
    return get_all()


@todo_app.post("/post", response_model=ToDOModel)
def post_todo(todo: ToDOModel) -> ToDOModel:
    try:
        created_todo = create(todo.model_dump())
        return created_todo
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@todo_app.put("/put", response_model=ToDOModel)
def put_todo(todo: ToDOModel) -> ToDOModel:
    try:
        updated = update(todo.model_dump(by_alias=True))
        if not updated.get("updated"):
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo
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
