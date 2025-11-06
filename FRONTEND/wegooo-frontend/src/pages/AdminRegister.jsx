import React, { useState } from "react";
import axios from "axios";
import "../styles/adminRegister.css";

const AdminRegister = () => {
  const [formData, setFormData] = useState({
    bus_name: "",
    travels_name: "",
    category: "",
    origin: "",
    destination: "",
    departure_time: "",
    arrival_time: "",
    fare_amount: "",
    total_seats: "",
  });

  // ✅ Added handleChange
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const departureDateTime = new Date(formData.departure_time);
      const arrivalDateTime = new Date(formData.arrival_time);

      const data = {
        bus_name: formData.bus_name,
        travels_name: formData.travels_name,
        category: formData.category,
        origin: formData.origin,
        destination: formData.destination,
        total_seats: formData.total_seats,
        departure_time: departureDateTime.toTimeString().split(" ")[0].slice(0, 5),
        arrival_time: arrivalDateTime.toTimeString().split(" ")[0].slice(0, 5),
        fare_amount: formData.fare_amount,
        travel_date: departureDateTime.toISOString().split("T")[0], // yyyy-mm-dd
      };

      const response = await axios.post("http://127.0.0.1:8000/api/register-bus/", data);

      if (response.status === 201 || response.status === 200) {
        alert("✅ Bus registered successfully!");
        setFormData({
          bus_name: "",
          travels_name: "",
          category: "",
          origin: "",
          destination: "",
          departure_time: "",
          arrival_time: "",
          fare_amount: "",
          total_seats: "",
        });
      } else {
        alert("❌ Error registering bus!");
      }
    } catch (error) {
      console.error("Error:", error.response?.data || error.message);
      alert("❌ Error registering bus! Check console for details.");
    }
  };

  return (
    <div className="max-w-lg mx-auto mt-10 p-6 shadow-lg rounded-lg bg-white">
      <h2 className="text-2xl font-bold mb-4 text-center">🚌 Register New Bus</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          name="bus_name"
          placeholder="Bus Name"
          onChange={handleChange}
          value={formData.bus_name}
          className="w-full border p-2 rounded"
        />
        <input
          name="travels_name"
          placeholder="Travels Name"
          onChange={handleChange}
          value={formData.travels_name}
          className="w-full border p-2 rounded"
        />

        <select
          name="category"
          onChange={handleChange}
          value={formData.category}
          className="w-full border p-2 rounded"
        >
          <option value="">Select Category</option>
          <option value="AC Seater">AC Seater</option>
          <option value="Non-AC Seater">Non-AC Seater</option>
          <option value="AC Sleeper">AC Sleeper</option>
          <option value="Non-AC Sleeper">Non-AC Sleeper</option>
        </select>

        <input
          name="origin"
          placeholder="From"
          onChange={handleChange}
          value={formData.origin}
          className="w-full border p-2 rounded"
        />
        <input
          name="destination"
          placeholder="To"
          onChange={handleChange}
          value={formData.destination}
          className="w-full border p-2 rounded"
        />

        <label>Departure Time:</label>
        <input
          type="datetime-local"
          name="departure_time"
          onChange={handleChange}
          value={formData.departure_time}
          className="w-full border p-2 rounded"
        />

        <label>Arrival Time:</label>
        <input
          type="datetime-local"
          name="arrival_time"
          onChange={handleChange}
          value={formData.arrival_time}
          className="w-full border p-2 rounded"
        />

        <input
          name="fare_amount"
          placeholder="Fare (₹)"
          type="number"
          onChange={handleChange}
          value={formData.fare_amount}
          className="w-full border p-2 rounded"
        />
        <input
          name="total_seats"
          placeholder="Total Seats"
          type="number"
          onChange={handleChange}
          value={formData.total_seats}
          className="w-full border p-2 rounded"
        />

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          Register Bus
        </button>
      </form>
    </div>
  );
};

export default AdminRegister;
