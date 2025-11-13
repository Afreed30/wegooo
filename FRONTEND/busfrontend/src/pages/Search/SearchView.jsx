import React, { useState } from "react";
import "./search.css"; // <-- add this

export default function SearchView({ onSearch }) {
  const [origin, setOrigin] = useState("");
  const [destination, setDestination] = useState("");
  const [date, setDate] = useState("");

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
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
        onChange={(e) => setDate(e.target.value)}
        required
      />

      <button className="search-btn">Search</button>
    </form>
  );
}
