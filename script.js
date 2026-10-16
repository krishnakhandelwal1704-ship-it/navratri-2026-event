function bookTicket(eventId, eventTitle, price, currency) {
  const bookingId = Math.floor(Math.random() * 9000) + 1000;
  const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=NAVRATRI-TICKET-BK-${bookingId}`;

  latestBooking = {
    id: `BK-${bookingId}`,
    title: eventTitle,
    name: currentUserName,
    phone: currentUserPhone,
    price: `${currency} ${price}`,
    qr: qrUrl,
  };

  userBookingsHistory.unshift({
    id: bookingId,
    title: eventTitle,
    qty: 1,
    total: price,
    currency: currency,
    date: new Date().toLocaleTimeString(),
  });

  document.getElementById("stat-total-bookings").innerText =
    userBookingsHistory.length;
  document.getElementById("stat-total-passes").innerText =
    userBookingsHistory.length;

  const listContainer = document.getElementById("dashboard-bookings-list");
  listContainer.innerHTML = "";
  userBookingsHistory.forEach((b) => {
    listContainer.innerHTML += `
                    <div class="bg-slate-50 p-3.5 rounded-2xl border border-slate-200 flex justify-between items-center text-sm">
                        <span class="font-bold text-slate-800">#${b.id} - ${b.title}</span>
                        <span class="text-orange-600 font-extrabold text-base">${b.currency} ${b.total}</span>
                    </div>
                `;
  });

  document.getElementById("booking-success-modal").classList.remove("hidden");
  document.getElementById("qr-code-img").src = qrUrl;
  document.getElementById("pass-details").innerText =
    `Booking #BK-${bookingId} | Pass Verified`;

  // WHATSAPP DIRECT CLICKABLE QR CODE LINK FORMAT
  const waText = encodeURIComponent(
    `🪔 NAVRATRI EVENT 2026 PASS 🪔\n\n👤 Name: ${currentUserName}\n📞 Phone: ${currentUserPhone}\n🎟️ Event: ${eventTitle}\n🔖 Booking ID: #BK-${bookingId}\n\n📲 Click below to open Gate Entry QR Code:\n${qrUrl}`,
  );

  document.getElementById("whatsapp-direct-btn").href =
    `https://wa.me/${currentUserPhone.replace("+", "")}?text=${waText}`;

  switchTab("dashboard");
}
