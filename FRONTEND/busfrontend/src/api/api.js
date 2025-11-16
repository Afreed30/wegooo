export const API_BASE_URL = "http://127.0.0.1:8000/api";

// Auto Inject Token into Headers
const authHeaders = () => {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Token ${token}` } : {};
};

export const api = {
  // ------------------------ AUTH ------------------------
  register: (data) =>
    fetch(`${API_BASE_URL}/register/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }).then((res) => res.json()),

  login: (data) =>
    fetch(`${API_BASE_URL}/login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }).then((res) => res.json()),

  logout: () =>
    fetch(`${API_BASE_URL}/logout/`, {
      method: "POST",
      headers: { ...authHeaders() },
    }),

  // ------------------------ BUS SEARCH ------------------------
  searchBuses: (origin, destination, date) =>
    fetch(
      `${API_BASE_URL}/search-buses/?origin=${origin}&destination=${destination}&travel_date=${date}`,
      { headers: { ...authHeaders() } }
    )
      .then((res) => res.json())
      .then((data) => {
        console.log("SEARCH RESPONSE:", data);
        return data;
      }),

  // ------------------------ SEATS ------------------------
  getSeats: (scheduleId) =>
    fetch(`${API_BASE_URL}/schedules/${scheduleId}/seats/`, {
      headers: { ...authHeaders() },
    }).then((res) => res.json()),

  // ------------------------ BOOKING ------------------------
  createBooking: (scheduleId, seatId, passenger) =>
  fetch(`${API_BASE_URL}/bookings/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
    },
    body: JSON.stringify({
      schedule: scheduleId,
      seat: seatId,
      passenger_name: passenger.passenger_name,
      passenger_age: passenger.passenger_age,
      passenger_gender: passenger.passenger_gender,
    }),
  }).then((res) => res.json()),


  getBookings: () =>
    fetch(`${API_BASE_URL}/bookings/`, {
      headers: { ...authHeaders() },
    }).then((res) => res.json()),

  // ------------------------ PAYMENT ------------------------
  createPaymentOrder: (bookingId) =>
  fetch(`${API_BASE_URL}/create-payment-order/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
    },
    body: JSON.stringify({ booking_id: bookingId }),
  }).then((res) => res.json()),


  verifyPayment: (data) =>
    fetch(`${API_BASE_URL}/verify-payment/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...authHeaders(),
      },
      body: JSON.stringify(data),
    }).then((res) => res.json()),
};
