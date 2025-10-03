from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, Enum as SQLEnum, Float
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum

# user table 
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True index=True)
    email = Column(String, unique=True, index=True, nullable=False) # should not be null
    name = Column(String)
    hashed_password = Column(String, nullable=False) 
    ingredients = relationship("Ingredient", back_populates="user")

class IngredientType(enum.Enum):
    MEAT = "meat"
    VEGETABLE = "vegetable"
    DAIRY = "dairy"
    GRAIN = "grain"
    FRUIT = "fruit"
    OTHER = "other"

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    type = Column(SQLEnum(IngredientType), nullable=False)
    measurement_unit = Column(String) # e.g., grams, liters, cups
    measurement_count = Column(Float) 
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="ingredients")



