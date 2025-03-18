from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from utils.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from utils.security import create_access_token, decode_access_token, hash_password, verify_password
from schemas import LoginRequest, LoginResponse, Token, UserResponse, CreateUserRequest
from typing import Annotated
from db import engine, SessionLocal

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import models
from models import User


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

# router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[SessionLocal, Depends(get_db)]
def authenticate_user(username: str, password: str, db):
     # 1. Find user by email
    user = db.query(models.User).filter(
        models.User.email == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # 2. Check the password
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    return user


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_request: CreateUserRequest, db: db_dependency):  # type: ignore
    # 1. Check if user already exists (by username or email)
    existing_user = db.query(User).filter(
        (User.email == user_request.email) |
        (User.username == user_request.username)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already in use."
        )

    # 2. Hash the incoming password
    hashed_pw = hash_password(user_request.password)

    # 3. Create the new user object
    new_user = User(
        username=user_request.username,
        email=user_request.email,
        firstname=user_request.firstname,
        lastname=user_request.lastname,
        hashed_password=hashed_pw,
        role=user_request.role,
        is_active=True
    )

    # 4. Add to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 5. Return the created user (response model excludes password)
    return new_user


@router.post("/login", response_model=LoginResponse)
def login(login_req: LoginRequest, db: db_dependency):  # type: ignore
    # 1. Find user by email
    try:
        user = authenticate_user(login_req.email, login_req.password, db)

        # 3. Create JWT token
        # We typically store user id (and maybe other data) in the token
        access_token_expires = timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # or timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=access_token_expires
        )

        # 4. Return the token + user data
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            # FastAPI will convert this using UserResponse (exclude password)
            user=user
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )
     
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency): # type: ignore
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    
    access_token_expires = timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # or timedelta(minutes=30)
    token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
        )

    return {'access_token': token, 'token_type': 'bearer'}


def get_current_user(
    db: db_dependency, # type: ignore
    # token: str = Depends(oauth2_scheme)
    token: Annotated[str, Depends(oauth2_scheme)]
) -> models.User:
    """
    1. Decode the token.
    2. Extract user_id from payload.
    3. Query the user in the database.
    4. Raise HTTPException if user not found or inactive.
    """
    payload = decode_access_token(token)
    user_id: int | None = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user_id claim",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(models.User).filter(models.User.id == user_id).first()
    print("user in get_current_user:", user.__dict__)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return user
