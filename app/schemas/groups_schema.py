from typing import List, Optional

from pydantic import BaseModel

from datetime import datetime

from app.util.schema import AllOptional



class Groups(BaseModel):
    id:int
    
    group_name:str
    
    created_by_id:int



    class Config:
        orm_mode = True

class get_groups(BaseModel):
    id:int
    
    group_name:str

    class Config:
        orm_mode = True
    
