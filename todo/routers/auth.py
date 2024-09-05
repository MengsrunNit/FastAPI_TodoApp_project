from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pytest import Session
from models import Users
from passlib.context import CryptContext
from database import sessionLocal
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.templating import Jinja2Templates
import os

router = APIRouter(
    prefix="/auth", 
    tags=['auth']
) 

SECRET_KEY = "8bca52e441e65da2f3e17bebf433f8abdff4f705be5652da06a24f46cef57643"
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token') #client will send this password

#create user Model 
class CreateUserRequest(BaseModel): 
    username: str
    email: str
    password: str
    firstname: str
    lastname: str 
    role: str
    phone_number: str
    

class Token(BaseModel): 
    access_token: str
    token_type : str


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        id: int = payload.get('id')
        role: str = payload.get('role')
        if username is None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': username, 'id': id, 'role': role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')


    
def create_access_token(username: str, user_id : int , role: str, expire_delta:timedelta): 
    #Input username and id into the token in oder to make it as a secure the info 
    # that nobody could know what is it by reading the inspect 
    encode ={'sub': username, "id": user_id, 'role': role }
    expire = datetime.now(timezone.utc) + expire_delta
    encode.update({"exp": expire})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


#get the database 
def get_db(): 
    db = sessionLocal()
    try: 
        yield db
    finally: 
        db.close()

#database dependency 
db_dependency = Annotated[Session, Depends(get_db)]

#bcrypt_context to decrept password in the database 
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")


# Initialize Jinja2Templates with the correct directory
templates = Jinja2Templates(directory="templates")

# Define the endpoint for rendering the login page
@router.get("/login", response_class=HTMLResponse)
async def render_login_page(request: Request): 
    return templates.TemplateResponse("login.html", {"request": request})
### EndPoint ###

@router.get("/register", response_class=HTMLResponse)
async def render_login_page(request: Request): 
    return templates.TemplateResponse("register.html", {"request": request})
### EndPoint ###


#user authendication 
def user_authendication(username:str, password: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()

    if not user: 
        return False
    if not bcrypt_context.verify(password, user.hashed_Password): 
        return False
    return user 
       


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      signupUser : CreateUserRequest): 
    signupUser2 = Users(
        username = signupUser.username, 
        email = signupUser.email, 
        firstname = signupUser.firstname, 
        lastname = signupUser.lastname, 
        role = signupUser.role,
        hashed_Password = bcrypt_context.hash(signupUser.password), 
        phone_number=signupUser.phone_number,  # Ensure this is set correctly
        is_active = True
    )
    db.add(signupUser2)
    db.commit()

   

@router.post("/token", response_model=Token)
async def login_auth_user(db: db_dependency, 
                      form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
                      ): 
    user = user_authendication(form_data.username, form_data.password, db)
    if not user: 
        return "Fail Authendicaiton"
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=15))

    return {'access_token': token, 'token_type': "bearer"}
    
    
