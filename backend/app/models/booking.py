from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.database.connection import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    
    ticket_quantity = Column(Integer, nullable=False, default=1)
    total_amount = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    
    # International User Details
    user_country = Column(String, nullable=False, default="India")
    payment_gateway = Column(String, nullable=False)  # e.g. "Stripe", "Razorpay", "PayPal"
    payment_status = Column(String, default="PENDING") # "SUCCESS", "FAILED"
    transaction_id = Column(String, unique=True, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())