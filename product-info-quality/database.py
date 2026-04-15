from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import DBModelBase

# Telling SQLAlchemy where to find the database file
DATABASE_URL = "sqlite:///test.db"

# Create the engine (the connection)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# This line looks at your models.py and creates the actual table in test.db
DBModelBase.metadata.create_all(engine)

# This creates a "Session" which is like an open phone line to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)