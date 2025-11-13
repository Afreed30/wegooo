import React from "react";
import "./header.css";
export default function Header({ user, setView, onLogout }) {
  return (
    <div className="header">
      <div className="header-left" onClick={() => setView("search")}>
        <img src="/PUBLIC/bus.png" className="logo" alt="Wegooo Bus Logo" />
        <span className="brand">Wegooo Bus</span>
      </div>

      <div className="header-right">
        <button onClick={() => setView("search")}>Search Bus</button>
        <button onClick={() => setView("bookings")}>My Bookings</button>

        {user ? (
          <>
            <span className="user">
              <span className="user-icon">🧑‍💼</span> {user.username}
            </span>
            <button className="logout" onClick={onLogout}>Logout</button>
          </>
        ) : (
          <button onClick={() => setView("login")}>Login</button>
        )}
      </div>
    </div>
  );
}
