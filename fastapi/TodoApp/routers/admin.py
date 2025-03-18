from fastapi import   APIRouter, Depends, Path, HTTPException, status
from utils.security import hash_password
from pydantic import BaseModel, Field
from typing import Annotated
from schemas import UpdateUserRequest
# from starlette import status
# import fastapi.TodoApp.models as models
import models
from db import engine, SessionLocal
from .auth import get_current_user
 
router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
 )

 
 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[SessionLocal, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/get-all-users", status_code=status.HTTP_200_OK)
async def get_all_users(user: user_dependency, db: db_dependency): # type: ignore
    if not user or user.role != "admin":
         raise HTTPException(status_code=401, detail="Authorization failed")
    return db.query(models.User).all()


@router.get("/get-all-todos", status_code=status.HTTP_200_OK)
async def get_all_todos(user: user_dependency, db: db_dependency): # type: ignore
    if  not user or user.role != "admin":
        raise HTTPException(status_code=401, detail="Authorization failed")
    return db.query(models.Todo).all()

@router.delete("/delete-all-todos", status_code=status.HTTP_200_OK)
async def delete_all_todos(user: user_dependency, db: db_dependency): # type: ignore
    if  not user or user.role != "admin":
        raise HTTPException(status_code=401, detail="Authorization failed")
    db.query(models.Todo).delete()
    db.commit()
    return
@router.put("/update-user", status_code=status.HTTP_200_OK)
async def update_user(payload: UpdateUserRequest, user: user_dependency, db: db_dependency): # type: ignore
    # 1. Check if current user is admin
    if not user or user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization failed: Only admins can update users."
        )

    # 2. Locate the user to update
    user_to_update = db.query(models.User).filter(models.User.id == payload.id).first()
    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {payload.id} not found."
        )
     # 3. Build a dictionary of updated fields, excluding any that were not provided
    update_data = payload.dict(exclude_unset=True)
    
    # If the admin wants to update the password, we should hash it
    if "password" in update_data:
        hashed = hash_password(update_data["password"])
        update_data["hashed_password"] = hashed

    # 4. Perform the update
    for field, value in update_data.items():
        setattr(user_to_update, field, value)

    db.commit()
    db.refresh(user_to_update)
    return user_to_update
