import os


ACCESS_TOKEN_EXPIRE_MINUTES= 30
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"