from typing import Annotated
from sqlalchemy.orm import Session 
from fastapi import Depends, HTTPException, Path, APIRouter
import models 
from database import sessionLocal
from models import Todos, Users
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(
    prefix="/user", 
    tags=['user']
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

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")

class UserVerification(BaseModel): 
    hash_password : str
    new_password: str

@router.get('/get_user')
async def get_user(db: db_dependency, 
                   user: user_dependency): 
    if user is None: 
        raise HTTPException(status_code=401, detail="User is not authendicated")
    todo_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if todo_model is None: 
        raise HTTPException(status_code=404, detail="User not Found")
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put('/change_password', status_code=status.HTTP_204_NO_CONTENT)
async def change_pass(db: db_dependency, 
                      user: user_dependency,
                      user_verified: UserVerification): 
    if user is None: 
        raise HTTPException(status_code=401, detail="User is not authendicated")
    todo_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if todo_model is None: 
        raise HTTPException(status_code=401, detail="User not Found")
    
    if not bcrypt_context.verify(user_verified.hash_password,todo_model.hashed_Password):
        raise HTTPException(status_code=401, detail="wrong password")

    todo_model.hashed_Password = bcrypt_context.hash(user_verified.new_password)

    db.commit()
    
    

    
    
    
