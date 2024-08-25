from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


#SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosApp.db'
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Mengsrun%4010@localhost/TodoApplicationDatabase'
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:Mengsrun%4010@127.0.0.1:3306/TodoAppDatabase'
engine = create_engine(SQLALCHEMY_DATABASE_URL)


#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
