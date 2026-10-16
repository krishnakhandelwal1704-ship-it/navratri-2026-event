from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database.connection import SessionLocal
from app.models.event import Event
from app.models.booking import Booking
from app.models.user import User
from app.utils.whatsapp import send_whatsapp_ticket  # WhatsApp integration

router = APIRouter(prefix="/bookings", tags=["Bookings"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class BookingCreate(BaseModel):
    user_id: int
    event_id: int
    ticket_quantity: int = 1
    user_country: str = "India"
    currency: str = "INR"
    payment_gateway: str = "Razorpay"

@router.post("/", status_code=status.HTTP_201_CREATED)
def book_ticket(
    booking_data: BookingCreate, 
    background_tasks: BackgroundTasks, # Fast response ke liye background task
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == booking_data.user_id).first()
    event = db.query(Event).filter(Event.id == booking_data.event_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if (event.total_capacity - event.tickets_sold) < booking_data.ticket_quantity:
        raise HTTPException(status_code=400, detail="Not enough tickets available")

    total_price = event.ticket_price * booking_data.ticket_quantity

    # Create Booking Record
    new_booking = Booking(
        user_id=booking_data.user_id,
        event_id=booking_data.event_id,
        ticket_quantity=booking_data.ticket_quantity,
        total_amount=total_price,
        currency=booking_data.currency,
        user_country=booking_data.user_country,
        payment_gateway=booking_data.payment_gateway,
        payment_status="SUCCESS"
    )

    event.tickets_sold += booking_data.ticket_quantity

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    # 🚀 Instant WhatsApp Notification in Background Task!
    if user.phone_number:
        background_tasks.add_task(
            send_whatsapp_ticket,
            to_phone=user.phone_number,
            booking_id=new_booking.id,
            event_title=event.title,
            ticket_qty=new_booking.ticket_quantity,
            total_amount=total_price,
            currency=booking_data.currency
        )

    return {
        "message": "Booking successful! Ticket confirmation WhatsApp par bhej di gayi hai.",
        "booking_id": new_booking.id,
        "total_amount": total_price,
        "currency": booking_data.currency,
        "whatsapp_sent_to": user.phone_number
    }