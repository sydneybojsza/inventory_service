from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from models import User, InventoryItem
from models.schemas import ItemCreate, Inventory

def add_item(db: Session, user_id: str, item: ItemCreate) -> Inventory:
    db_item = db.query(InventoryItem).filter(InventoryItem.user_id == user_id, InventoryItem.item_name == item.item_name).first()
    if db_item:
        db_item.quantity += item.quantity
    else:
        db_item = InventoryItem(user_id=user_id, item_name=item.item_name, quantity=item.quantity)
        db.add(db_item)
    db.commit()
    db.refresh(db_item)
    user = db.query(User).filter(User.id == user_id).first()
    return {"items": user.inventory} if user else {"items": []}

def add_items(db: Session, user_id: str, items: List[ItemCreate]) -> Inventory:
    for item in items:
        add_item(db=db, user_id=user_id, item=item)
    user = db.query(User).filter(User.id == user_id).first()
    return {"items": user.inventory} if user else {"items": []}

def get_inventory(db: Session, user_id: str) -> Inventory:
    user = db.query(User).filter(User.id == user_id).first()
    return {"items": user.inventory} if user else {"items": []}

def subtract_item(db: Session, user_id: str, item: ItemCreate) -> Inventory:
    db_item = db.query(InventoryItem).filter(InventoryItem.user_id == user_id, InventoryItem.item_name == item.item_name).first()
    if db_item and db_item.quantity >= item.quantity:
        db_item.quantity -= item.quantity
        if db_item.quantity == 0:
            db.delete(db_item)
        db.commit()
        db.refresh(db_item)
    elif not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    elif db_item.quantity < item.quantity:
        raise HTTPException(status_code=400, detail="Not enough items in inventory")
    user = db.query(User).filter(User.id == user_id).first()
    return {"items": user.inventory} if user else {"items": []}
