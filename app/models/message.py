from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from app.models.base_model import BaseModel
from datetime import datetime


class Message(BaseModel, table=True):
    __tablename__ = "messages"
    __table_args__ = {'extend_existing': True}
    

    # id: int = Field(default=None, primary_key=True

    content: str = Field()
    sender_id: int = Field(foreign_key="user.id")

    
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    group_id:int=Field(foreign_key="groups.id")

    # Relationship back to User
    user: Optional["User"] = Relationship(back_populates="messages")
    groups: Optional["Groups"] = Relationship(back_populates="messages")  # s

    