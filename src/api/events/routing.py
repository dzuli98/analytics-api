import os
from typing import List
from api.db.session import get_session
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from timescaledb.hyperfunctions import time_bucket
from .models import (
    EventModel,
    EventBucketSchema,
    EventListSchema,
    EventCreateSchema,
    EventUpdateSchema,
    get_utc_now
)
 
router = APIRouter()

DEFAULT_LOOKUP_PAGES = ['/about', '/contact', '/pages', '/pricing']

# GET /api/events/
@router.get("/", response_model=List[EventBucketSchema])
def read_events(
    duration: str = Query('1 day'),
    pages: List[str] = Query(default=None),
    session: Session = Depends(get_session)
    ):
    bucket = time_bucket(duration, EventModel.time)
    lookup_pages = pages if isinstance(pages, list) and len(pages) > 0 else DEFAULT_LOOKUP_PAGES
    query = (
        select(
            bucket.label('bucket'),
            EventModel.page.label('page'),
            func.count().label('count')
        )
        .where(
            EventModel.page.in_(pages))
        .group_by(bucket, EventModel.page)
        .order_by(bucket.desc(), EventModel.page )
    )
    results = session.exec(query).fetchall()
    return results


# SEND DATA HERE
# CREATE VIEW
# POST /api/events 
@router.post("/", response_model= EventModel)
def create_event(payload: EventCreateSchema, 
                 session: Session = Depends(get_session)):
    # a bunch of rows
    data = payload.model_dump() # dict
    obj = EventModel.model_validate(data) # takes raw data and turns it into a validated, typed Pydantic model 
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return  obj


@router.get("/{event_id}", response_model=EventModel)
def get_event(event_id: int, session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if result:
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Event with {event_id} does not exit!')

# Update data
# PUT /api/events/10
@router.put("/{event_id}", response_model=EventModel)
def update_event(event_id: int, payload: EventUpdateSchema,
                 session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    obj = session.exec(query).first() # type = EventModel
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Event with {event_id} does not exit!')
    data = payload.model_dump()
    for k, v in data.items():
        if k == 'id':
            continue
        setattr(obj, k, v)
    obj.updated_at = get_utc_now()
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return  obj
