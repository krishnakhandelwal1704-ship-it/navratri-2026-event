import os
from twilio.rest import Client

# Twilio Credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "YOUR_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "YOUR_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

# Global Client Object Definition
client = None
if TWILIO_ACCOUNT_SID != "YOUR_ACCOUNT_SID" and TWILIO_AUTH_TOKEN != "YOUR_AUTH_TOKEN":
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    except Exception as e:
        print(f"Twilio Client Init Error: {e}")

def send_whatsapp_ticket(to_phone: str, booking_id: int, event_title: str, ticket_qty: int, total_amount: float, currency: str):
    qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=NAVRATRI-TICKET-BK-{booking_id}"
    
    message_body = (
        f"🎉 *NAVRATRI 2026 - SECURE ENTRY PASS* 🎉\n\n"
        f"Aapki booking successfully confirm ho gayi hai!\n\n"
        f"🎫 *Booking ID:* #{booking_id}\n"
        f"💃 *Event:* {event_title}\n"
        f"🎟️ *Quantity:* {ticket_qty} Ticket(s)\n"
        f"💳 *Total Paid:* {currency} {total_amount}\n\n"
        f"📱 *Gate Security QR Pass:* {qr_code_url}\n\n"
        f"Shubh Navratri! Venue par yeh pass dikhayein. ✨"
    )

    try:
        if client:
            formatted_phone = to_phone if to_phone.startswith("+") else f"+91{to_phone}"
            message = client.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                body=message_body,
                to=f"whatsapp:{formatted_phone}"
            )
            print(f"WhatsApp Message Sent! SID: {message.sid}")
            return True
        else:
            print(f"[Simulated WhatsApp Delivery to {to_phone}]: Pass Created for Booking #{booking_id}")
            return True
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")
        return False