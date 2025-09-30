import React, { useState } from "react";
import api from "../../api/api";
import "../../i18n"
import { useTranslation } from "react-i18next";

export default function LoginForm({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username || !password) return alert("Fill all fields");

    setLoading(true);
    setError(null);

    try {
      // Adjust endpoint if your backend uses a different route (e.g. "auth/token/" or "login/")
      const res = await api.post("token/", { username, password });

      // Expecting { access, refresh } or { token } depending on backend
      const { access, refresh, token } = res.data;

      // Store tokens where src/api/api.ts looks for them
      if (access || token) {
        localStorage.setItem("access_token", access || token);
      }
      if (refresh) {
        localStorage.setItem("refresh_token", refresh);
      }

      // Notify parent with username + tokens (App will persist user state)
      if (onLogin) onLogin({ username, access: access || token, refresh });
    } catch (err) {
      console.error("Login error:", err);
      setError("Login failed. Check credentials or try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="login-form" onSubmit={handleSubmit}>
      <label>Username</label>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Enter Username"
      />

      <label>Password</label>
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Enter password"
      />

      <div className="auth-actions">
        <button type="submit" className="primary-btn" disabled={loading}>
          {loading ? "Signing in..." : "Login"}
        </button>
        <button
          type="button"
          className="secondary-btn"
          onClick={() => alert("Sign up not implemented yet")}
        >
          Sign up
        </button>
      </div>

      {error && <div style={{ color: "crimson", marginTop: 8 }}>{error}</div>}
    </form>
  );
}
