from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True, future=True) # get the database and create an engine

SessionLocal = sessionmaker(
    bind=engine,  # to read from the database
    expire_on_commit=False, # to not expire the session after commit, save state in cache no need to query again
)

# from now on if the model class inherits from Base, it will be mapped to a database table
# create a declarative base class to define the database models

session = SessionLocal()