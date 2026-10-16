from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.sql import func
from app.database.connection import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)  # Garba Night, Dandiya Night, Virtual Pass, etc.
    description = Column(String, nullable=True)
    
    # Timing & Location
    date_time = Column(DateTime(timezone=True), nullable=False)
    venue = Column(String, nullable=False)
    country = Column(String, default="India")
    timezone = Column(String, default="Asia/Kolkata")  # UTC / EST / IST support
    is_virtual = Column(Boolean, default=False)        # Virtual/Online stream link for abroad users
    
    # Pricing & International Payment Details
    ticket_price = Column(Float, nullable=False)
    currency = Column(String, default="INR")           # INR, USD, EUR, GBP etc.
    
    # Capacity & Sales Tracker
    total_capacity = Column(Integer, nullable=False)
    tickets_sold = Column(Integer, default=0)
    
    # Media & Metadata
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())