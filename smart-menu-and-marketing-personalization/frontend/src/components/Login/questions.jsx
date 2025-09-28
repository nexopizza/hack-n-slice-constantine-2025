import React from "react";
import "./questions.css";

export default function Questions({ onClose }) {
  return (
    <div className="questions-wrap">
      <header className="questions-header">
        <h3>Quick questionnaire</h3>
        <button className="close-btn" onClick={onClose}>✕</button>
      </header>

      <div className="questions-body">
                      {/* Placeholder backend will add actual questions later ADD THEM >:( */}
        <p className="muted">Questions will be added here.</p>
      </div>

      <div className="questions-actions">
        <button className="primary-btn" onClick={onClose}>Done</button>
      </div>
    </div>
  );
}