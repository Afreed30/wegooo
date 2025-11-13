import React, { useState, useEffect } from "react";
import Header from "./components/Header";
import { api } from "./api/api";
import "./app.css";
import SearchView from "./pages/Search/SearchView";
import ResultsView from "./pages/Results/ResultsView";
import SeatsView from "./pages/Seats/SeatsView";
import PassengerView from "./pages/Passenger/PassengerView";
import Login from "./pages/Auth/Login";
import Register from "./pages/Auth/Register";
import PaymentView from "./pages/Payment/PaymentView";
import BookingsView from "./pages/Bookings/BookingsView";
import TicketPreview from "./pages/TicketPreview/TicketPreview";
import MergedBusSunsetBackground from "./BusCityBackground";

export default function App() {
  const [view, setView] = useState(localStorage.getItem("view") || "search");
  const [user, setUser] = useState(JSON.parse(localStorage.getItem("user")));
  const [token, setToken] = useState(localStorage.getItem("token"));

  const [results, setResults] = useState([]);
  const [schedule, setSchedule] = useState(null);
  const [seats, setSeats] = useState([]);
  const [picked, setPicked] = useState(null);

  const [passenger, setPassenger] = useState(null);
  const [booking, setBooking] = useState(null);
  const [bookings, setBookings] = useState([]);
  const [previewBooking, setPreviewBooking] = useState(null);


  const handleLogin = async (u, p) => {
    const data = await api.login({ username: u, password: p });
    if (data.token) {
      setUser(data.user);
      setToken(data.token);
      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify(data.user));
      setView("search");
    }
  };

  const handleRegister = async (data) => {
    const res = await api.register(data);
    if (res.token) {
      setUser(res.user);
      setToken(res.token);
      localStorage.setItem("token", res.token);
      localStorage.setItem("user", JSON.stringify(res.user));
      setView("search");
    }
  };

  const logout = () => {
  localStorage.clear();
  setToken(null);
  setUser(null);
  localStorage.setItem("view", "search"); // ✅ Force redirect after refresh
  setView("search");
};


 const handleSearch = async (o, d, t) => {
  const data = await api.searchBuses(o, d, t);

  // ✅ Ensure `results` is always an array
  setResults(Array.isArray(data) ? data : []);

  setView("results");
};



  const selectBus = async (bus) => {
    setSchedule(bus);
    setSeats(await api.getSeats(bus.id));
    setView("seats");
  };

  useEffect(() => {
    const handler = () => book();
    window.addEventListener("seat.proceed", handler);
    return () => window.removeEventListener("seat.proceed", handler);
  }, [picked]);

  const book = async () => {
    if (!token) return setView("login");
    if (!picked) return alert("Please select a seat.");
    setView("passenger"); // ✅ move to passenger details
  };

  const createBooking = async (details) => {
  const data = await api.createBooking(
    token,
    schedule.id,
    picked.id,
    {
      passenger_name: details.name,
      passenger_age: details.age,
      passenger_gender: details.gender,
    }
  );

  if (data.id) {
    setBooking(data);
    setView("payment");
  } else {
    alert(data.error || "Booking failed");
  }
};


  const handlePayment = async () => {
    if (!booking) return;

    const orderData = await api.createPaymentOrder(token, booking.id);

    const rzp = new window.Razorpay({
      key: orderData.key,
      amount: orderData.amount,
      currency: orderData.currency,
      order_id: orderData.order_id,
      name: "Bus Ticket Booking",
      handler: async (response) => {
        await api.verifyPayment(token, {
          razorpay_payment_id: response.razorpay_payment_id,
          razorpay_order_id: response.razorpay_order_id,
          razorpay_signature: response.razorpay_signature,
          booking_id: booking.id,
        });

        alert("✅ Payment Successful! Your ticket is confirmed.");
        setView("bookings");
      },
    });

    rzp.open();
  };

  const loadBookings = async () => {
    setBookings(await api.getBookings(token));
  };

  useEffect(() => {
    if (view === "bookings" && token) loadBookings();
  }, [view]);

  useEffect(() => {
  localStorage.setItem("view", view);
}, [view]);


  return (
    <div>
      <MergedBusSunsetBackground />
      <Header user={user} setView={setView} onLogout={logout} />
      <div className="app-container">
        {view === "search" && <SearchView onSearch={handleSearch} />}
        {view === "results" && (
  <ResultsView results={results} onSelectBus={selectBus} setView={setView} />
)}


        {view === "seats" && (
          <SeatsView seats={seats} schedule={schedule} picked={picked} setPicked={setPicked} />
        )}

       {view === "passenger" && (
  <PassengerView
    picked={picked}
    schedule={schedule}
    onSubmit={(details) => createBooking(details)}
  />
)}

{previewBooking && (
  <TicketPreview
    booking={previewBooking}
    onClose={() => setPreviewBooking(null)}
  />
)}


        {view === "login" && <Login onLogin={handleLogin} switchToRegister={() => setView("register")} />}
        {view === "register" && <Register onRegister={handleRegister} switchToLogin={() => setView("login")} />}
        {view === "payment" && <PaymentView booking={booking} onPay={handlePayment} />}
        {view === "bookings" && (
  token ? (
    <BookingsView bookings={bookings} setPreviewBooking={setPreviewBooking} />
  ) : (
    (() => {
      alert("Please login to view your bookings");
      setView("login");
      return null;
    })()
  )
)}


      </div>
    </div>
  );
}
