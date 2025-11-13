import "./payment.css"; // 

export default function PaymentView({ booking, onPay }) {
  if (!booking) return null;

  return (
    <div className="payment-box">
      <h3 className="payment-title">Booking #{booking.id}</h3>

      <p className="payment-seat">
        Seat: <span>{booking.seat_details?.seat_number}</span>
      </p>

      <p className="payment-price">₹{booking.price}</p>

      <button onClick={onPay} className="payment-btn">
        Pay & Confirm Booking
      </button>

      <p className="payment-note">Secure payment powered by Razorpay</p>
    </div>
  );
}
