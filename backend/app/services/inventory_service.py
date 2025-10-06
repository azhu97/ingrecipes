from sqlalchemy.orm import Session
from app.models import models
from fastapi import HTTPException

# add an ingredient to a user's inventory list, wether new or existing 
def add_item_to_user_inventory(db: Session, user_id: int, ingredient_id: int, quantity: int, unit: str = "serving"):
    user = db.query(models.User).filter(models.User.id == user_id).first() # get user by id 
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    ingredient = db.query(models.Ingredient).filter(models.Ingredient.id == ingredient_id).first() # get ingredient by id
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

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
        raise HTTPException(status_code=404, detail="User not found")
    
    return db.query(models.UserInventory).filter(models.UserInventory.user_id == user_id).all()

# remove an item from a user's inventory list 
def remove_ingredient_from_user_inventory(db: Session, user_id: int, ingredient_id: int):
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

# update the quantity of an ingredient in a user's inventory list 
def update_ingredient_quantity(db: Session, user_id: int, ingredient_id: int, new_quantity: float):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    ingredient = db.query(models.Ingredient).filter(models.Ingredient.id == ingredient_id).first()
    if not user or not ingredient:
        raise HTTPException(status_code=404, detail="User or Ingredient not found")
    
    inventory_item = db.query(models.UserInventory).filter(
        models.UserInventory.user_id == user_id,
        models.UserInventory.ingredient_id == ingredient_id
    ).first()
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    if new_quantity > 0:
        inventory_item.quantity = new_quantity
    else:
        db.delete(inventory_item) # remove item, delete the relationship between user and ingredient
    
    db.commit()
    db.refresh(inventory_item) if new_quantity > 0 else None
    return inventory_item if new_quantity > 0 else None




    

