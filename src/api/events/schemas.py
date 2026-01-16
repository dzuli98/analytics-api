from pydantic import BaseModel, Field
from typing import List, Optional

"""
id
path
description
Those will be stored in database, but with schemas we control
which data is supported by endpoints!
"""

class EventSchema(BaseModel):
    id: int
    page: Optional[str] =  ""
    description: Optional[str] = ""

class EventCreateSchema(BaseModel):
    page: str
    description: Optional[str] = Field(default='')

class EventUpdateSchema(BaseModel):
    description: str

class EventListSchema(BaseModel):
    results: List[EventSchema]
    count: int