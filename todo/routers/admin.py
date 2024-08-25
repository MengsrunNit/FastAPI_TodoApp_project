from typing import Annotated
from sqlalchemy.orm import Session 
from fastapi import Depends, HTTPException, Path, APIRouter
import models 
from database import sessionLocal
from models import Todos
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user


router = APIRouter(
    prefix="/admin", 
    tags=['admin']
)


class TodoRequest(BaseModel): 
    title: str = Field(min_length=3)
    description: str = Field(min_length = 3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool 


def get_db(): 
    db = sessionLocal()
    try: 
        yield db
    finally: 
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/todo')
async def read_all(db:db_dependency, user: user_dependency): 
    
    if user is None or user.get('role') != "admin": 
        raise HTTPException(status_code= 404, detail=("Cannot 1 Authedicate the user "))

    all_user = db.query(Todos).all()
    if all_user is None: 
        raise HTTPException(status_code= 404, detail=("Cannot 2 Authedicate the user "))

    return all_user

@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def admin_remove(db:db_dependency, 
                    user: user_dependency, 
                    todo_id: int = Path(gt=0)): 

    if user is None or user.get('role') != "admin": 
        raise HTTPException(status_code= 401, detail=("Cannot 1 Authedicate the user "))
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None: 
        raise HTTPException(status_code= 404, detail=("Cannot 2 Authedicate the user "))
    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()
    


    
    

            



