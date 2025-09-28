import React from 'react';
import { User, Coins } from "lucide-react";
import Logo from '../../assets/Logo.png';
import './header.css';

const Header = ({ coins, onAvatarClick, onLogoClick }) => {
  return (
    <header className="header">
      <div className="logo">
        <button onClick={onLogoClick} className="logo-btn">
          <img src={Logo} alt="App Logo" className="logo-img" />
        </button>
      </div>

      <div className="right-side">
        <div className="coin-container">
          <Coins className="coin-icon" />
          <span className="coin-number">{coins}</span>
        </div>
        <div className="avatar" onClick={onAvatarClick}>
          <User className="icon" />
        </div>
      </div>
    </header>
  );
};

export default Header;
