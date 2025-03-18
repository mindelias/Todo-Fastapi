# schemas.py
from typing import Optional
from pydantic import BaseModel, EmailStr



class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"  # Forward reference if UserResponse not defined yet

class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: EmailStr
    firstname: str
    lastname: str
    role: str

class UpdateUserRequest(BaseModel):
    id: int
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    role: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    firstname: str
    lastname: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    complete: bool
    priority: int
    class Config:
        from_attributes = True

class TodoRequest(BaseModel):
    title: str
    description: str
    priority: int
    complete: bool

    class Config:
        from_attributes = True

LoginResponse.model_rebuild()