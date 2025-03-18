from fastapi import   APIRouter, Depends, Path, HTTPException, status
from pydantic import BaseModel, Field
from typing import Annotated
# from starlette import status
# import fastapi.TodoApp.models as models
import models
from db import engine, SessionLocal
from .auth import get_current_user
 
router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
 )

 
 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_annotation = Annotated[SessionLocal, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str 
    description: str
    priority: int
    complete: bool

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    complete: bool
    priority: int

    class Config:
        from_attributes = True


@router.get("/")
async def get_todos_by_user(user: user_dependency, db:   db_annotation): # type: ignore
    if  not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    print(f"user: {user}")
    return db.query(models.Todo).filter(models.Todo.user_id == user.id).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo(user: user_dependency, db:  db_annotation, todo_id: int = Path(..., gt=0)):  # type: ignore
    if  not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).filter(models.Todo.user_id == user.id).first()
    if  not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_annotation, todo: TodoRequest): # type: ignore
    if  not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    todo = models.Todo(**todo.dict(), user_id=user.id)

    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@router.put("/todo/{todo_id}",  status_code=status.HTTP_200_OK, response_model=TodoResponse)
async def update_todo(user: user_dependency,db: db_annotation,  payload: TodoRequest, todo_id: int = Path(..., gt=0)): # type: ignore
    if  not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).filter(models.Todo.user_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.title = payload.title
    todo.description = payload.description
    todo.priority = payload.priority
    todo.complete = payload.complete
    db.commit()
    return todo



@router.delete("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(user: user_dependency, db: db_annotation, todo_id: int = Path(..., gt=0)): # type: ignore
    if  not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).filter(models.Todo.user_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()



# @app.put("/todo/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
# async def update_todo(
#     todo_id: Annotated[int, Path(gt=0)],
#     payload: TodoRequest,
#     db: Session = Depends(get_db)
# ):
#     todo = db.query(models.Todo).get(todo_id)
#     if not todo:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

#     for attr, value in payload.dict().items():
#         setattr(todo, attr, value)

#     db.commit()
#     db.refresh(todo)  # ensures the returned object has updated data from the database
#     return todo

# @app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_todo(
#     todo_id: Annotated[int, Path(gt=0)],
#     db: Session = Depends(get_db)
# ):
#     todo = db.query(models.Todo).get(todo_id)
#     if not todo:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

#     db.delete(todo)
#     db.commit()
    






# app.include_router(todo.router)
# app.include_router(user.router)