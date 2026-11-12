from sqlmodel import create_engine , Session , SQLModel
from sqlalchemy.orm import sessionmaker , declarative_base
from sqlalchemy import create_engine
import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.engine import URL
from sqlmodel import create_engine

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
elif os.getenv("DB_USER"):
    url = URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 5432)),
        database=os.getenv("DB_NAME"),
    )

    engine = create_engine(url)
else:
    engine = create_engine("sqlite:///./local.db")

#env_path = Path(__file__).resolve().parent / ".env"
#load_dotenv(dotenv_path=env_path)
#DATABASE_URL = os.getenv("DATABASE_URL")
#load_dotenv()
#url = URL.create(

    #drivername="postgresql+psycopg" ,
    #username="postgres",
    #password="Sh......",
    ##port=5432,
    #database="mlstore")


#DATABASE_URL = os.getenv("DATABASE_URL")



#if not DATABASE_URL:
    #raise ValueError("url missing ")


#engine = create_engine(DATABASE_URL , pool_pre_ping = True)

#def create_db_and_tables():
    #SQLModel.metadata.create_all(engine)


#def get_session():
    #with Session(engine) as session:
        #yield session





def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session