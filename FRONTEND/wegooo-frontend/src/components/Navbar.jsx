import React, { useState } from "react";
import { Link } from "react-router-dom";
import "../styles/navbar.css";

const Navbar = () => {
  const [showAccount, setShowAccount] = useState(false);

  return (
    <nav className="navbar">
      <h2 className="logo">Wegoo</h2>
      <div className="nav-links">
        <Link to="/" className="nav-link">Home</Link>
        <button 
          className="nav-link account-btn"
          onClick={() => setShowAccount(!showAccount)}
        >
          Account ⬇
        </button>
        <Link to="/admin/register" className="register-btn">Register Bus</Link>
      </div>

      {showAccount && (
        <div className="account-dropdown">
          <Link to="/account/login" className="dropdown-item">Login</Link>
          <Link to="/account/signup" className="dropdown-item">Signup</Link>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
