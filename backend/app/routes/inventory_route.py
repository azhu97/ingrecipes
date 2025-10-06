from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
import app.services.inventory_service as inventory_service
import app.services.user_service as user_service

router = APIRouter(
    prefix = "/inventory",
    tags = ["inventory"]
)

# get inventory items by user id
@router.get("/user/{user_id}")
def get_inventory_by_user_id(user_id: int, db: Session = Depends(get_db)) -> list[inventory_service.models.InventoryItem]:
    items = inventory_service.get_inventory_by_user_id(db=db, user_id=user_id)
    if not items:
        raise HTTPException(status_code=404, detail="No inventory items found for this user")
    return items

# add inventory item
@router.post("/user/{user_id}/add")
def add_inventory_item(user_id: int, ingredient_id: int, quantity: int, unit: str = "serving", db: Session = Depends(get_db)) -> inventory_service.models.InventoryItem:
    item = inventory_service.add_item_to_user_inventory(db=db, user_id=user_id, ingredient_id=ingredient_id, quantity=quantity, unit=unit)
    return item

# remove inventory item
@router.delete("/user/{user_id}/remove")
def remove_inventory_item(user_id: int, ingredient_id: int, db: Session = Depends(get_db)) -> dict:
    success = inventory_service.remove_ingredient_from_user_inventory(db=db, user_id=user_id, ingredient_id=ingredient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return {"message": "Inventory item successfully removed"}

# update inventory item quantity 
@router.put("/user/{user_id}/update")
def update_inventory_item_quantity(user_id: int, ingredient_id: int, quantity: int, db: Session = Depends(get_db)) -> inventory_service.models.InventoryItem:
    item = inventory_service.update_inventory_item_quantity(db=db, user_id=user_id, ingredient_id=ingredient_id, quantity=quantity)
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return item