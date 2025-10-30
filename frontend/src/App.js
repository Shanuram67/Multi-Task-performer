// App.jsx (FIXED for jwt-decode v4+)
import React, { useState, useEffect } from "react";
import LoginPage from "./components/Login";
import Dashboard from "./components/Dashboard";
import "./App.css";
import { jwtDecode } from "jwt-decode"; // ✅ Updated import syntax

export default function App() {
  const [user, setUser] = useState(null);

useEffect(() => {
  const token = localStorage.getItem("access_token");
  if (token) {
    try {
      const decoded = jwtDecode(token);
      const expiry = decoded.exp * 1000;
      if (Date.now() < expiry) {
        const storedUser = localStorage.getItem("current_username");
        if (storedUser) setUser(storedUser);
      } else {
        localStorage.clear();
      }
    } catch (err) {
      console.error("Invalid token:", err);
      localStorage.clear();
    }
  }
}, []);



  const handleLogin = (username, token) => {
    localStorage.setItem("access_token", token);
    localStorage.setItem("current_username", username);
    setUser(username);
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("current_username");
    setUser(null);
  };

  return (
    <div className="app-container">
      {user ? (
        <Dashboard user={user} onLogout={handleLogout} />
      ) : (
        <LoginPage onLogin={handleLogin} />
      )}
    </div>
  );
}
