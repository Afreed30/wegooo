import React, { useState } from "react";
import "./passenger.css";

export default function PassengerView({ picked, schedule, onSubmit }) {
  const [form, setForm] = useState({
    name: "",
    age: "",
    gender: "",
  });

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });
  console.log("FULL SCHEDULE =", schedule);
  console.log("FULL PICKED =", picked);

  return (
    <div className="passenger-box">
      <h2 className="passenger-title">Passenger Details</h2>

      <div className="passenger-field">
        <label>Passenger Name</label>
        <input name="name" onChange={handleChange} required />
      </div>

      <div className="passenger-field">
        <label>Age</label>
        <input type="number" name="age" onChange={handleChange} required />
      </div>

      <div className="passenger-field">
        <label>Gender</label>
        <select name="gender" onChange={handleChange} required>
          <option value="">Select</option>
          <option value="M">Male</option>
          <option value="F">Female</option>
        </select>
      </div>

      <div className="passenger-summary">
        Seat: <strong>{picked?.seat_number}</strong> • Bus:{" "}
        {schedule?.bus_details?.name}
      </div>

      <button className="passenger-btn" onClick={() => onSubmit(form)}>
        Continue to Payment
      </button>
    </div>
  );
}
