import React, { useState } from "react";
import "./login.css";
export default function Login({ onLogin, switchToRegister }) {
  const [username, setU] = useState("");
  const [password, setP] = useState("");
  const [error, setError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setError(false);
      setErrorMessage("");

      const response = await onLogin(username, password);  
      // onLogin must return error if login fails

      if (!response.success) {
        setErrorMessage(response.error || "Invalid credentials");
        setError(true);

        setTimeout(() => setError(false), 800);
      }

    } catch (err) {
      setErrorMessage("Login failed");
      setError(true);

      setTimeout(() => setError(false), 800);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="login-box">
      <h2 className="login-title">Login</h2>

      <input
        className={`login-input ${error ? "input-error" : ""}`}
        placeholder="Username"
        onChange={(e) => setU(e.target.value)}
        required
      />

      <input
        type="password"
        className={`login-input ${error ? "input-error" : ""}`}
        placeholder="Password"
        onChange={(e) => setP(e.target.value)}
        required
      />

      {errorMessage && (
        <p className="error-text">{errorMessage}</p>
      )}

      <button className="login-btn">Login</button>

      <p className="login-text">
        No account?{" "}
        <button type="button" className="login-link" onClick={switchToRegister}>
          Register
        </button>
      </p>
    </form>
  );
}
