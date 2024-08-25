from database import Base 
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey



class Users(Base): 
    __tablename__= "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique = True)
    email = Column(String, unique=True)
    firstname = Column(String)
    lastname = Column(String)
    hashed_Password = Column(String)
    is_active = Column(Boolean, default=True)
   
    role = Column(String)
    phone_number = Column(String)

class Todos(Base): 
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default= False)
    owner_id = Column(Integer, ForeignKey('users.id'))
