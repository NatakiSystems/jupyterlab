from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import DBModelBase

# This creates a file named test.db in your folder
DATABASE_URL = "sqlite:///test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# This creates the tables based on your models.py
DBModelBase.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)