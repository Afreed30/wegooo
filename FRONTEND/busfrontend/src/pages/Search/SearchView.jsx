import React, { useState } from "react";
import "./search.css";

export default function SearchView({ onSearch }) {
  const [origin, setOrigin] = useState("");
  const [destination, setDestination] = useState("");
  const [date, setDate] = useState("");

  const today = new Date().toISOString().split("T")[0]; 

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();

        const selectedDate = new Date(date);
        const todayDate = new Date();
        todayDate.setHours(0, 0, 0, 0);

        // ❌ Past date safety check
        if (selectedDate < todayDate) {
          onSearch(origin, destination, []);
          return;
        }

        onSearch(origin, destination, date);
      }}
      className="search-box"
    >
      <h2 className="search-title">Search Buses</h2>

      <input
        className="search-input"
        placeholder="From"
        onChange={(e) => setOrigin(e.target.value)}
        required
      />

      <input
        className="search-input"
        placeholder="To"
        onChange={(e) => setDestination(e.target.value)}
        required
      />

      <input
        type="date"
        className="search-input"
        min={today}   
        onChange={(e) => setDate(e.target.value)}
        required
      />

      <button className="search-btn">Search</button>
    </form>
  );
}
