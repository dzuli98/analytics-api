import os
from typing import List
from api.db.session import get_session
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from sqlalchemy import func, case
from datetime import datetime, timedelta, timezone
from timescaledb.hyperfunctions import time_bucket
from .models import (
    EventModel,
    EventBucketSchema,
    EventListSchema,
    EventCreateSchema,
    get_utc_now
)
 
router = APIRouter()

DEFAULT_LOOKUP_PAGES = pages = ['/about', '/contact', '/pages', '/pricing', '/home', '/blog', '/features']

# GET /api/events/
@router.get("/", response_model=List[EventBucketSchema])
def read_events(
    duration: str = Query('1 day'),
    pages: List[str] = Query(default=None),
    session: Session = Depends(get_session)
    ):
    os_case = case(
        (EventModel.user_agent.ilike('%windows%'), 'Windows'),
        (EventModel.user_agent.ilike('%mac%'), 'MacOS'),
        (EventModel.user_agent.ilike('%linux%'), 'Linux'),
        (EventModel.user_agent.ilike('%android%'), 'Android'),
        (EventModel.user_agent.ilike('%iphone%'), 'iOS'),
        else_='Other'
    ).label('operating_system')
    bucket = time_bucket(duration, EventModel.time)
    lookup_pages = pages if isinstance(pages, list) and len(pages) > 0 else DEFAULT_LOOKUP_PAGES
    query = (
        select(
            bucket.label('bucket'),
            os_case,
            EventModel.page.label('page'),
            func.count().label('count')
        )
        .where(
            EventModel.page.in_(lookup_pages))
        .group_by(
            bucket,
            EventModel.page,
            os_case
            )
        .order_by(
            bucket.desc(),
            EventModel.page,
            os_case
            )
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
