import  King  from "../assets/King.png"

export default function Header(){
    return(
        <header>
          <img src= { King }  alt="logo" />
          <h1>Nexo InOuty</h1>
          <nav>
            <a href="#home">Home</a>
            <a href="#about">ClockIn</a>
            <a href="#home">Planning</a>
            <a href="#about">Reporting</a>
          </nav>
          <button className="newDay">
              New day 
          </button>
        </header>
    )
}