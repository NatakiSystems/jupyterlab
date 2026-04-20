import json
from sqlalchemy import Column, Integer, String, DateTime, Text, Numeric
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# This creates the "Base" that all our models will follow
DBModelBase = declarative_base()

class Product(DBModelBase):
    __tablename__ = "products"

    # Defining the columns (fields) for our table
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    attributes = Column(Text, nullable=True) # This stores extra details like battery life as text
    information_score = Column(Integer, nullable=False, default=0)
    barcode = Column(Numeric, nullable=False, default=0)
    price = Column(String(255), nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Helper function to save a Python dictionary into the database
    def set_attributes(self, data: dict):
        self.attributes = json.dumps(data)

    # Helper function to turn that database text back into a Python dictionary
    def get_attributes(self) -> dict:
        if not self.attributes:
            return {}
        return json.loads(self.attributes)