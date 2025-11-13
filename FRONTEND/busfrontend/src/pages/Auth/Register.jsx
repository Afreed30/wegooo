import React, { useState } from "react";
import "./register.css"; // <-- add this

export default function Register({ onRegister, switchToLogin }) {
  const [form, setForm] = useState({});

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onRegister(form);
      }}
      className="register-box"
    >
      <h2 className="register-title">Create Account</h2>

      {["username", "email", "password", "password2"].map((name) => (
        <input
          key={name}
          name={name}
          placeholder={name}
          onChange={(e) =>
            setForm({ ...form, [e.target.name]: e.target.value })
          }
          className="register-input"
          type={name.includes("password") ? "password" : "text"}
          required
        />
      ))}

      <button className="register-btn">Register</button>

      <p className="register-text">
        Already have an account?{" "}
        <button type="button" onClick={switchToLogin} className="register-link">
          Login
        </button>
      </p>
    </form>
  );
}
