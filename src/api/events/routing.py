from fastapi import APIRouter
from .schemas import (
    EventSchema,
    EventListSchema,
    EventCreateSchema,
    EventUpdateSchema
)

router = APIRouter()

# GET /api/events/
@router.get("/")
def read_events() -> EventListSchema:
    # a bunch of rows
    return {
        "results": [
            {"id": 1}, {"id": 2} , {"id": 3}
        ],
        "count": 3
    }

# SEND DATA HERE
# CREATE VIEW
# POST /api/events 
@router.post("/")
def create_event(payload: EventCreateSchema) -> EventSchema:
    # a bunch of rows
    data = payload.model_dump()
    print('!!!!!!!!!!', type(data))
    print('!!!!!!!!!', {**data})
    print(payload)
    print(type(payload))
    return  {"id": 1, **data}


@router.get("/{event_id}")
def get_event(event_id: int) -> EventSchema:
    # a single row
    return {"id": event_id}

# Update data
# PUT /api/events/10
@router.put("/{event_id}")
def update_event(event_id: int, payload: EventUpdateSchema) -> EventSchema:
    # a single row
    print(payload)
    return {"id": event_id}

'''
# Update data
# DELETE /api/events/10
@router.delete("/{event_id}")
def delete_event(event_id: int, payload: dict={}) -> EventSchema:
    # a single row
    return {"id": event_id}
'''