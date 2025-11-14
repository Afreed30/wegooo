import React from "react";
import "./results.css";

export default function ResultsView({ results, onSelectBus, setView }) {
  // If no buses found
  if (!results || results.length === 0) {
    return (
      <div className="no-results-box">

        {/* 😭 Crying Passenger Animation */}
        <div className="crying-passenger">
          😭
        </div>

        <h2 className="no-results-title">No Buses Found</h2>
        <p className="no-results-text">
          Sorry, there are no buses available for the selected route and date.
        </p>

        <button className="no-results-btn" onClick={() => setView("search")}>
          Return to Home
        </button>
      </div>
    );
  }

  return (
    <div className="results-list">
      {results.map((s) => (
        <div key={s.id} className="result-card">

          <div>
            <div className="bus-name">{s.bus_details.name}</div>
            <div className="sub-text">
              Bus No: <span>{s.bus_details.bus_number}</span>
            </div>
            <div className="sub-text">
              Category: <span>{s.bus_details.category_name}</span>
            </div>
            <div className="route">
              {s.route_details.origin} → {s.route_details.destination}
            </div>
          </div>

          <div className="price">₹{s.fare_amount}</div>

          <button className="select-seat-btn" onClick={() => onSelectBus(s)}>
            Select Seats
          </button>
        </div>
      ))}
    </div>
  );
}
