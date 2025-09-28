import React, { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import { UserRoundCheck, ShoppingBag, ChevronDown, ChevronUp, Phone } from "lucide-react";
import { useTranslation } from "react-i18next"; 
import LoginForm from "./loginForm";
import Questions from "./questions";
import "./Login.css";
import "./questions.css";

const sections = [
  { title: "Account Info", icon: <UserRoundCheck />, items: ["Profile", "Coins & rewards", "Delete Account"] },
  { title: "My Orders", icon: <ShoppingBag />, items: ["Order History", "Upcoming Orders"] },
  { title: "Support", icon: <Phone />, items: ["+213 ---------", "FAQs"] },
];

export default function LoginSidebar({ isOpen, onClose, user, onLogin, onLogout }) {
  const { t, i18n } = useTranslation();
  const [openSections, setOpenSections] = useState([0, 1]);
  const [promptShown, setPromptShown] = useState(false);
  const [showQuestionPrompt, setShowQuestionPrompt] = useState(false);
  const [showQuestions, setShowQuestions] = useState(false);

  useEffect(() => {
    // when user becomes logged-in and we haven't shown prompt this session, show it
    if (user && !promptShown) {
      setShowQuestionPrompt(true);
      setPromptShown(true);
    }
  }, [user, promptShown]);

  useEffect(() => {
    if (!user) {
      // reset prompt state on logout
      setPromptShown(false);
      setShowQuestionPrompt(false);
      setShowQuestions(false);
    }
  }, [user]);

  const handleLoginLocal = (creds) => {
    if (onLogin) onLogin(creds);
    // keep prompt logic here
  };

  const handleLogoutLocal = () => {
    if (onLogout) onLogout();
    // local reset handled by useEffect up there
  };

  const toggleSection = (idx) => {
    setOpenSections((prev) => (prev.includes(idx) ? prev.filter((i) => i !== idx) : [...prev, idx]));
  };

  const handleLanguageChange = (lang) => {
    i18n.changeLanguage(lang);
    localStorage.setItem("sm_lang", lang);
  };

  return (
    <div className={`sidebar ${isOpen ? "open" : ""}`}>
      <div className="sidebar-header">
        <h2 className="sidebarFont">{user ? t("Hi", { name: user },"!") : t("Welcome Customer !")}</h2>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          {user && <button className="logout-btn" onClick={handleLogoutLocal}>{t("Sign Out")}</button>}
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>
      </div>

      <div className="sidebar-content">
        {!user ? (
          <div className="auth-panel">
            <p className="auth-intro">{t("Login Intro")}</p>
            <LoginForm onLogin={handleLoginLocal} />
          </div>
        ) : showQuestions ? (
          <Questions onClose={() => setShowQuestions(false)} />
        ) : (
          sections.map((section, idx) => (
            <div key={section.title} className="sidebar-section">
              <div
                className="section-title"
                onClick={() => toggleSection(idx)}
                style={{ cursor: section.items.length ? "pointer" : "default" }}
              >
                <span className="section-icon">{section.icon}</span>
                {section.title}
                {section.items.length > 0 && (
                  <span className="arrow">
                    {openSections.includes(idx) ? <ChevronUp size={18} color="#f97316" /> : <ChevronDown size={18} color="#f97316" />}
                  </span>
                )}
              </div>

              <div className={`section-panel ${openSections.includes(idx) ? "open" : ""}`}>
                {section.items.length > 0 && (
                  <ul className="section-list">
                    {section.items.map((item, i) => (
                      <li key={item} style={{ ["--delay"]: `${i * 45}ms` }}>{item}</li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      <div className="sidebar-language">
        <label htmlFor="language-select">{t("Language :")}</label>
       <button className="languageButton">
        <select
          id="language-select"
          value={i18n.language || "en"}
          onChange={(e) => handleLanguageChange(e.target.value)}
        >
          <option value="en">English</option>
          <option value="fr">Français</option>
          <option value="ar">العربية</option>
        </select>
        </button>
      </div>

      {/* Questionnaire model*/}
      {showQuestionPrompt &&
        createPortal(
          <div className="question-modal-backdrop" onMouseDown={() => setShowQuestionPrompt(false)}>
            <div className="question-modal" onMouseDown={(e) => e.stopPropagation()}>
              <h3>{t("questionnaireTitle")}</h3>
              <p className="muted">{t("questionnairePrompt")}</p>
              <div className="question-actions">
                <button
                  className="primary-btn"
                  onClick={() => {
                    setShowQuestionPrompt(false);
                    setShowQuestions(true);
                  }}
                >
                  {t("Yes")}
                </button>
                <button className="secondary-btn" onClick={() => setShowQuestionPrompt(false)}>
                  {t("Remind me later")}
                </button>
              </div>
            </div>
          </div>,
          document.body
        )}
    </div>
  );
}
