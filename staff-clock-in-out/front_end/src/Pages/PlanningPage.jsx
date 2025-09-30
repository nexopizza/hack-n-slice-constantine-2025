import Header from "../Components/Header"
import DropDownList from "../Components/DropDownList"
import "../index.css"
import { useState } from "react"
import ShiftsDropDownList from "../Components/ShiftDropDownList"

export default function Planning(){
    // Planning Modal(Dialog box) 
    const [isOpen, setIsOpen] = useState(false);
    const [field1, setField1] = useState("");
    const [field2, setField2] = useState("");
    const employees = [
    {
      name: "Akram Dib",
    },
    {
      name: "Alaa krem",
    },
    {
      name: "Diaa Chouai",
    },
    {
      name: "Djelil Bestandji",
    },
    {
      name: "Djemel Helleli",
    },
    {
      name: "Djemel Mehres",
    },
    {
      name: "Farid Djebbar",
    },
    {
      name: "Heithem Boura",
    },
    {
      name: "Heithem Dadesi",
    },
    {
      name: "Ilyes Houari",
    },
    {
      name: "Ismail Cheniti",
    },
    {
      name: "Moncef Boulekzez",
    },
    {
      name: "Mohamed Bouafia",
    },
    {
      name: "Rafik Souiki",
    },
    {
      name: "Riad Telidjene",
    },
    {
      name: "Rochdi Djenhi",
    },
    {
      name: "Taha Ferradji",
    },
    {
      name: "Tedjeddine Bououdine",
    },
    {
      name: "Yaacoub Benmessi",
    },
    {
      name: "Zakaria Fileli",
    },
    {
      name: "Ziad Zeid",
    }
    ];
    const shifts=[{num:"1"}, {num:"2"}, {num:"3"}];
    return(
        <>
            <Header /> 
            <div
            style={{
                display: "flex",
                justifyContent: "flex-start",
                alignItems: "center",
                color: "black",
                fontSize: "30px",
                marginLeft:"35px",
                marginTop: "40px",
                marginBottom: "0px",
            }}
            >
               Planning Table: 
            </div>
            <div
            style={{
                display: "flex",
                justifyContent: "flex-start",
                alignItems: "center",
                color: "black",
                fontSize: "14px",
                marginLeft:"35px",
                marginTop: "5px",
                marginBottom: "0px",
            }}
            >
               Organize and display work shifts clearly for efficient scheduling and operations management 
            </div>
             
            <div>
            <table border="1" cellPadding="20" cellSpacing="0">
            <thead>
            <tr>
                <th>Posts/Shifts</th>
                <th>6:00-14:00 (1)</th>
                <th>20:00-16:00 (2)</th>
                <th>16:00-00:00 (3)</th>
                <th>Operations</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td style={{background:"linear-gradient(to right, #EB4219, #F6892A)", color: "white"}}>Pizzaiolo</td>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <td><button className="edit-btn" onClick={() => setIsOpen(true)}> Edit </button></td>
            </tr> 
             <tr>
                <td style={{background:"linear-gradient(to right, #EB4219, #F6892A)", color: "white"}}>Livreur</td>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <td><button className="edit-btn" onClick={() => setIsOpen(true)}> Edit </button></td>
            </tr>  
             <tr>
                <td style={{background:"linear-gradient(to right, #EB4219, #F6892A)", color: "white"}}>Agent polyvalent</td>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <td><button className="edit-btn" onClick={() => setIsOpen(true)}> Edit </button></td>
            </tr> 
            <tr>
                <td style={{background:"linear-gradient(to right, #EB4219, #F6892A)", color: "white"}}>Prepateur</td>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <td><button className="edit-btn" onClick={() => setIsOpen(true)}> Edit </button></td>
            </tr> 
            <tr>
                <td style={{background:"linear-gradient(to right, #EB4219, #F6892A)", color: "white"}}>Cassier</td>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <td><button className="edit-btn" onClick={() => setIsOpen(true)}> Edit </button></td>
            </tr>
            <tr>
                <td style={{background:"linear-gradient(to right, #EB4219, #F6892A)", color: "white"}}>Serveur</td>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <td><button className="edit-btn" onClick={() => setIsOpen(true)}> Edit </button></td>
            </tr> 
            <tr>
                <td style={{background:"linear-gradient(to right, #EB4219, #F6892A)", color: "white"}}>Plongeur</td>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <td><button className="edit-btn" onClick={() => setIsOpen(true)}> Edit </button></td>
            </tr> 
            <tr>
                <td style={{background:"linear-gradient(to right, #EB4219, #F6892A)", color: "white"}}>Manageur</td>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <td><button className="edit-btn" onClick={() => setIsOpen(true)}> Edit </button></td>
            </tr>
            <tr>
                <td style={{background:"linear-gradient(to right, #EB4219, #F6892A)", color: "white"}}>Packaging</td>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <td><button className="edit-btn" onClick={() => setIsOpen(true)}> Edit </button></td>
            </tr>
            <tr>
                <td style={{background:"linear-gradient(to right, #EB4219, #F6892A)", color: "white"}}>Topping</td>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <td><button className="edit-btn" onClick={() => setIsOpen(true)}> Edit </button></td>
            </tr>
            <tr>
                <td style={{background:"linear-gradient(to right, #EB4219, #F6892A)", color: "white"}}>Bar</td>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <DropDownList employees={ employees }/>
                <td><button className="edit-btn" onClick={() => setIsOpen(true)}> Edit </button></td>
            </tr>     
            </tbody>
            </table>
            {isOpen && (
            <div className="dialog-backdrop">
              <div className="dialog-box">
            <h3
            style={{
              textAlign: "center",
              marginTop: "0",
              background: "linear-gradient(to right, #EB4219, #F6892A, #F36224, #EB4219)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent"
            }}
            >
              Edit Box
            </h3>
            <div className="modal">
              <ShiftsDropDownList Shifts={ shifts }/>
              <DropDownList employees={ employees }/>
            </div>
            <div style={{ textAlign: "center", marginTop:"30px"}}>
              <button className="edit-btn" onClick={() => setIsOpen(false)}>Close</button>
              
              <button className="edit-btn" onClick={() => alert(`Values: ${field1}, ${field2}`)}> Save </button>
        
            </div>
            </div>
            </div>
            )}

            </div>
            
        </>
    )
}