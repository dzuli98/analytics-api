from sqlmodel import SQLModel, Field
from typing import List, Optional
import sqlmodel
from datetime import datetime, timezone
from timescaledb import TimescaleModel  # Import TimescaleModel for time-series capabilities
from timescaledb.utils import get_utc_now

# page visits at any given time

class EventModel(TimescaleModel, table = True):
    page: str = Field(index=True)
    user_agent: Optional[str] = Field(default="", index=True)
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True)
    session_id: Optional[str] = Field(index=True)
    duration: Optional[int] = Field(default=0)  # duration in seconds

    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 3 months"

class EventCreateSchema(SQLModel):
    page: str
    user_agent: Optional[str] = Field(default="", index=True)
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True)
    session_id: Optional[str] = Field(index=True)
    duration: Optional[int] = Field(default=0)  # duration in seconds

class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int

class EventBucketSchema(SQLModel):
    bucket: datetime
    page: str
    user_agent: Optional[str] = ""
    operating_system: Optional[str] = ""
    count: int