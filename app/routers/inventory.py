from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from db import crud
from models.schemas import ItemCreate, Inventory
from dependencies import get_db, get_current_user

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.post("/add_item/", response_model=Inventory)
def add_item_to_inventory(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
) -> Inventory:
    return crud.add_item(db=db, user_id=current_user, item=item)


@router.post("/add_items/", response_model=Inventory)
def add_items_to_inventory(
    items: List[ItemCreate],
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
) -> Inventory:
    return crud.add_items(db=db, user_id=current_user, items=items)


@router.get("/", response_model=Inventory)
def get_inventory(
    db: Session = Depends(get_db), current_user: str = Depends(get_current_user)
) -> Inventory:
    return crud.get_inventory(db=db, user_id=current_user)


@router.post("/subtract_item/", response_model=Inventory)
def subtract_item_from_inventory(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
) -> Inventory:
    return crud.subtract_item(db=db, user_id=current_user, item=item)
