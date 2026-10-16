from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.event import Event

router = APIRouter(prefix="/events", tags=["Events"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return events