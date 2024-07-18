from pydantic import BaseModel, Field
from typing import List


class ItemCreate(BaseModel):
    item_name: str = Field(min_length=1, max_length=100, pattern="^[a-zA-Z0-9 ]+$")
    quantity: int = Field(ge=0)


class InventoryItem(BaseModel):
    item_name: str
    quantity: int

    model_config = {"from_attributes": True}


class Inventory(BaseModel):
    items: List[InventoryItem]

    model_config = {"from_attributes": True}
