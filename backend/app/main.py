from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import engine, Base, SessionLocal
from app.models.event import Event
from app.routers import auth, events, bookings
from datetime import datetime

# Create Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NAVRATRI 2026 Smart Event Platform")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(bookings.router)

# Automatically create default events on startup
@app.on_event("startup")
def create_default_events():
    db = SessionLocal()
    if db.query(Event).count() == 0:
        events_list = [
            Event(
                title="Royal Dandiya Night 2026",
                category="VIP Garba",
                description="Featuring live celebrity singer & traditional orchestra.",
                date_time=datetime(2026, 10, 18, 19, 30, 0),
                venue="Vrindavan Lawns, Jaipur",
                country="India",
                timezone="Asia/Kolkata",
                ticket_price=750.0,
                currency="INR",
                total_capacity=1500,
                image_url="https://images.unsplash.com/photo-1599839575945-a9e5af0b3aa5"
            ),
            Event(
                title="Global Dandiya Beats - London Pass",
                category="International",
                description="Direct live streaming & physical pass for London arena.",
                date_time=datetime(2026, 10, 19, 20, 0, 0),
                venue="Wembley Arena, London",
                country="UK",
                timezone="Europe/London",
                ticket_price=25.0,
                currency="GBP",
                total_capacity=800,
                image_url="https://images.unsplash.com/photo-1514525253161-7a46d19cd819"
            )
        ]
        db.add_all(events_list)
        db.commit()
    db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to NAVRATRI 2026 API"}