from fastapi import FastAPI
import models
from db import engine
from routers import todo, auth, admin

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)