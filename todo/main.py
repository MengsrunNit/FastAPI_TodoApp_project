from typing import Annotated
from sqlalchemy.orm import Session 
from fastapi import FastAPI, Request, Response
import models 
from database import engine, sessionLocal
from routers import auth, todo, admin, user
from fastapi.templating import Jinja2Templates
import os
from fastapi.staticfiles import StaticFiles 


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

# templates = Jinja2Templates(directory = "todoApp/todo/templates")
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory = static_dir), name = "static")

@app.get("/")
def homeindex(request: Request): 
    return templates.TemplateResponse("index.html", {"request": request})




app.include_router(todo.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(user.router)


