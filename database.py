from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# CREATE DATABASE ENGINE
engine = create_engine("sqlite:///todo.db")

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
