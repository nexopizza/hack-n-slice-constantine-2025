import { Link } from "react-router-dom";
import King from "../assets/King.png";


export default function Header() {
  return (
    <header>
      <img src={King} alt="logo" />
      <h1>Nexo InOuty</h1>
      <nav className="navbar">
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/clock-in">Clockin</Link></li>
          <li><Link to="/planning">Planning</Link></li>
          <li><Link to="/reporting">Reporting</Link></li>
        </ul>
      </nav>
      <button className="newDay">New Day</button>
    </header>
  );
}
