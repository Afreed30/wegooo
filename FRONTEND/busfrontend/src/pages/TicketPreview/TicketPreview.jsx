import "./TicketPreview.css";
import QRCode from "react-qr-code";

export default function TicketPreview({ booking, onClose }) {
  if (!booking) return null;

  const downloadLink = `http://127.0.0.1:8000/api/bookings/${booking.id}/ticket/pdf/`;

  const qrValue = `Wego Bus Ticket | Booking #${booking.id} | Seat ${booking.seat_details.seat_number}`;

  return (
    <div className="tp-overlay">
      <div className="tp-card">

        <img src="/bus.png" alt="Wegooo" className="tp-logo" />

        <h2 className="tp-title">WEGOOO BUS TICKET</h2>

        <div className="tp-details">
          <div><b>Passenger:</b> {booking.passenger_name}</div>
          <div><b>Bus:</b> {booking.schedule_details.bus_details.name}</div>
          <div><b>Route:</b> {booking.schedule_details.route_details.origin} → {booking.schedule_details.route_details.destination}</div>
          <div><b>Date:</b> {booking.schedule_details.travel_date}</div>
          <div><b>Seat:</b> {booking.seat_details.seat_number}</div>
        </div>

        <h3 className="tp-price">₹{booking.price}</h3>

        <div className="tp-qr">
          <QRCode value={qrValue} size={90} />
        </div>

       <button
  className="tp-download"
  onClick={() => {
    const token = localStorage.getItem("token");

    fetch(downloadLink, {
      method: "GET",
      headers: {
        Authorization: `Token ${token}`,
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Download failed");
        return res.blob();
      })
      .then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `Wegooo_Ticket_${booking.id}.pdf`;
        a.click();
        window.URL.revokeObjectURL(url);
      })
      .catch((err) => console.error(err));
  }}
>
  Download PDF
</button>

        <button className="tp-close" onClick={onClose}>
          ✕
        </button>

      </div>
    </div>
  );
}
