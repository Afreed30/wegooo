import "./bookings.css";

export default function BookingsView({ bookings,setPreviewBooking }) {
  console.log("BOOKINGS →", bookings);
  return (
    <div className="bookings-container">

      {bookings.map((b) => (
        <div key={b.id} className="booking-card">

          <div className="booking-header">
            <div className="booking-id">Booking #{b.id}</div>

            <div className={`status-badge ${b.status.toLowerCase()}`}>
              {b.status}
            </div>
          </div>

          <div className="booking-details">
            <div><span>Passenger:</span> {b.passenger_name || "-"}</div>
            <div><span>Bus:</span> {b.schedule_details?.bus_details?.name || "-"}</div>
            <div><span>Route:</span> {b.schedule_details?.route_details?.origin || "-"} → {b.schedule_details?.route_details?.destination || "-"}</div>
            <div><span>Date:</span> {b.schedule_details?.travel_date || "-"}</div>
            <div><span>Seat:</span> {b.seat_details?.seat_number || "-"}</div>
          </div>
          <div className="booking-footer">
            <div className="booking-price">₹{b.price}</div>

            {b.status === "CONFIRMED" && (
              <button
  className="ticket-btn"
  onClick={() => setPreviewBooking(b)}
>
  View / Download Ticket
</button>

            )}
          </div>

        </div>
      ))}

      {bookings.length === 0 && (
        <p className="no-bookings">No bookings found.</p>
      )}
    </div>
  );
}
