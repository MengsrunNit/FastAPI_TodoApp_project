from typing import Annotated
from sqlalchemy.orm import Session 
from fastapi import FastAPI, Request
import models 
from database import engine, sessionLocal
from routers import auth, todo, admin, user


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(todo.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(user.router)


