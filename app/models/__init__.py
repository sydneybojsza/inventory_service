from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    password = Column(String)
    inventory = relationship("InventoryItem", back_populates="owner")


class InventoryItem(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    item_name = Column(String, index=True)
    quantity = Column(Integer)

    owner = relationship("User", back_populates="inventory")
