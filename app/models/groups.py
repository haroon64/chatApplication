

from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from app.models.base_model import BaseModel
from datetime import datetime



class Groups(BaseModel, table=True):
    __tablename__ = "groups"

    # id: int = Field(default=None, primary_key=True)


    group_name:str = Field()
    created_by_id:int=Field(foreign_key="user.id")

    user: Optional["User"] = Relationship(back_populates="groups")
    messages: List["Message"] = Relationship(back_populates="groups")