from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum as SQLEnum, Float
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum

# User table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(100))
    hashed_password = Column(String, nullable=False)

    # one user -> many inventory items
    inventory_items = relationship("UserInventory", back_populates="user")

class IngredientType(enum.Enum):
    MEAT = "meat"
    VEGETABLE = "vegetable"
    DAIRY = "dairy"
    GRAIN = "grain"
    FRUIT = "fruit"
    OTHER = "other"

# Ingredient table
class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), index=True, nullable=False)
    description = Column(Text)
    type = Column(SQLEnum(IngredientType), nullable=False)

    # one ingredient -> many user inventories
    user_inventories = relationship("UserInventory", back_populates="ingredient")

class UserInventory(Base):
    __tablename__ = "user_inventories"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)
    measurement_unit = Column(String(50), nullable=False)
    quantity = Column(Float, nullable=False)

    # relations 
    user = relationship("User", back_populates="inventory_items")
    ingredient = relationship("Ingredient", back_populates="user_inventories")
