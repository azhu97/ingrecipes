from sqlalchemy.orm import Session
from app.models import models

# add an ingredient to a user's inventory list, wether new or existing 
def add_item_to_user_inventory(db: Session, user_id: int, ingredient_id: int, quantity: int, unit: str = "serving"):
    user = db.query(models.User).filter(models.User.id == user_id).first() # get user by id 
    if not user:
        raise ValueError("User not found")

    ingredient = db.query(models.Ingredient).filter(models.Ingredient.id == ingredient_id).first() # get ingredient by id
    if not ingredient:
        raise ValueError("Ingredient not found")
    
    inventory_item = db.query(models.UserInventory).filter(
        models.UserInventory.user_id == user_id,
        models.UserInventory.ingredient_id == ingredient_id
    ).first() # check if item is already in inventory

    if inventory_item:
        inventory_item.quantity += quantity # update quantity if exists
    else: # not in inventory, create new entry
        new_ingredient = models.UserInventory(
            user_id = user_id,
            ingredient_id = ingredient_id,
            measurement_unit = unit,
            quantity = quantity
        )
        db.add(new_ingredient)

    db.commit()
    db.refresh(inventory_item) if inventory_item else db.refresh(new_ingredient)
    return inventory_item if inventory_item else new_ingredient

# get all inventory items for a user
def get_user_inventory(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first() # check if given user_id exists
    if not user:
        raise ValueError("User not found")
    
    return db.query(models.UserInventory).filter(models.UserInventory.user_id == user_id).all()

# remove an item from a user's inventory list 
def remove_item_from_user_inventory(db: Session, user_id: int, ingredient_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first() # get user by id

    ingredient = db.query(models.Ingredient).filter(models.Ingredient.id == ingredient_id).first() # get ingredient by id
        
    if not user or not ingredient:
        return False
    
    inventory_item = db.query(models.UserInventory).filter(
        models.UserInventory.user_id == user_id,
        models.UserInventory.ingredient_id == ingredient_id
    ).first()
    if not inventory_item:
        return False
    
    db.delete(inventory_item)
    db.commit()
    return True 

    
    

