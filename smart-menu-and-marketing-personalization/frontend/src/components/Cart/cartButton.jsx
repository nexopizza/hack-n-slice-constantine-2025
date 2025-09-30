import React from "react";
import { ShoppingBag } from "lucide-react"; 


//the cart is just an idea for design, no functionality yet :D
export default function CartButton({ itemCount }) {
  return (
    <button
      style={{
        position: "fixed",
        bottom: "20px",
        right: "20px",
        backgroundColor: "rgb(239, 64, 0)",
        color: "white",
        border: "none",
        borderRadius: "50%",
        width: "60px",
        height: "60px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: "18px",
        cursor: "pointer",
        boxShadow: "0 4px 8px rgba(0,0,0,0.2)",
      }}
    >
      <ShoppingBag size={24} />
      {itemCount > 0 && (
        <span
          style={{
            position: "absolute",
            top: "10px",
            right: "10px",
            background: "white",
            color: "#ff6b6b",
            borderRadius: "50%",
            padding: "2px 6px",
            fontSize: "12px",
            fontWeight: "bold",
          }}
        >
          {itemCount}
        </span>
      )}
    </button>
  );
}
