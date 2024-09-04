from typing import Annotated
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session 
from fastapi import Depends, HTTPException, Path, APIRouter, Request, status
import models 
from database import sessionLocal
from models import Todos
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user
from fastapi.templating import Jinja2Templates

###Import Jinja2Template directory ####

templates = Jinja2Templates(directory="templates")



router = APIRouter(
    prefix="/todo",
    tags= ['databaseApp']
)


class TodoRequest(BaseModel): 
    title: str = Field(min_length=3)
    description: str = Field(min_length = 3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = Field(default=False)


def get_db(): 
    db = sessionLocal()
    try: 
        yield db
    finally: 
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

def redirect_to_login(): 
    redirect_response = RedirectResponse(url = "/auth/login", status_code = status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response

# ##### Pages #######
@router.get("/todo-page",response_class=HTMLResponse)
async def todoPage(request:Request, db: db_dependency): 
    try: 
        token = request.cookies.get('access_token')
        user = await get_current_user(token)

        if user is None: 
            print("Hello world")
            return templates.TemplateResponse("register.html", {"request": request})
        
        todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

        return templates.TemplateResponse("todo.html", {"request": request, "todos": todos, "user": user,})

    except Exception as e:
        # Log the exception if needed
        print(f"An error occurred: {e}")
        return redirect_to_login()
    

#########End Page#####
@router.get("/add-todo",response_class=HTMLResponse)
async def addtodoPage(request:Request): 
     return templates.TemplateResponse("add-to.html", {"request": request})
    

#########End Page#####





@router.get('/')
async def read_all(db:db_dependency, user: user_dependency): 
    return db.query(Todos).filter(Todos.owner_id ==  user.get("id")).all()

@router.get("/todo/{todo_id}", status_code= status.HTTP_200_OK)
async def read_todo(db:db_dependency, 
                    user: user_dependency,
                    todo_id: int = Path(gt=0)): 

    if user is None: 
        raise HTTPException(status_code=401, detail="authendication fail")
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None: 
        return todo_model
    raise HTTPException(status_code = 404, detail='To do not Found')


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency,
                      todo_request: TodoRequest, 
                      user: user_dependency
                      ): 
    if user is None: 
        raise HTTPException(status_code=401, detail="authendication fail")
    
    todo_model = Todos(**todo_request.model_dump(), owner_id = user.get('id'))

    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}")
async def update_todo(db: db_dependency, 
                       todo_request: TodoRequest,
                       user: user_dependency,
                       todo_id: int): 
    
    if user is None: 
        raise HTTPException(status_code=401, detail="authendication fail")
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None: 
        raise HTTPException(status_code = 404, detail='To noooot Found')
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

@router.delete("/todo/{todo_id}")
async def delete_task(db: db_dependency, 
                      user: user_dependency, 
                      todo_id: int):
    if user is None: 
        raise HTTPException(status_code=401, detail="authendication fail")
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None: 
        raise HTTPException(status_code = 404, detail='To not Found')
    
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()

    db.commit()
    
    

    
