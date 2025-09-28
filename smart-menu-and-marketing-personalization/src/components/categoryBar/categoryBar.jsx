import React, { useRef } from "react";
import "./categoryBar.css";
import {
  ChevronLeft,
  ChevronRight,
  Coffee,
  Heart,
  Pizza,
  Salad,
  IceCream,
  CupSoda,
  Croissant,
} from "lucide-react";

import dessertSVG from "../../assets/dessert.svg";
import Drinks from "../../assets/Drinks.svg";
import bakerySVG from "../../assets/bakery.svg";


const categoriesOrder = [
  "For you",
  "Pizzas",
  "Salads",
  "Desserts",
  "Drinks",
  "Hot Drinks",
  "Gelato",
  "Bakery",
];

const lucideMap = {
  "For you": Heart,
  Pizzas: Pizza,
  Salads: Salad,
  "Hot Drinks": Coffee,
  Gelato: IceCream,
  Drinks: CupSoda,
  Bakery: Croissant,
};


const svgMap = {
  Desserts: dessertSVG,
  Bakery: bakerySVG,
};

const CategoryBar = ({ selectedCategory, onCategoryChange }) => {
  const containerRef = useRef(null);

  const scroll = (direction) => {
    if (!containerRef.current) return;
    const scrollAmount = 200;
    containerRef.current.scrollBy({
      left: direction === "left" ? -scrollAmount : scrollAmount,
      behavior: "smooth",
    });
  };

  return (
    <div className="category-bar">
      <button className="scroll-btn left" onClick={() => scroll("left")}>
        <ChevronLeft size={20} color="rgba(255,255,255,0.95)" />
      </button>

      <div className="category-container" ref={containerRef}>
        {categoriesOrder.map((name) => {
          const IconComp = lucideMap[name];
          const svgSrc = svgMap[name];
          const isActive = selectedCategory === name;
          const itemClass = `category-item ${isActive ? "active" : ""}`;

          return (
            <div
              key={name}
              onClick={() => onCategoryChange(name)}
              className={itemClass}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === "Enter") onCategoryChange(name);
              }}
            >
              <div className="category-icon-wrap" aria-hidden>
                {IconComp ? (
                  <IconComp
                    size={20}
                    stroke="currentColor"
                    color="none"
                    className="category-lucide"
                    aria-hidden
                  />
                ) : svgSrc ? (
                  <img src={svgSrc} alt={name} className="category-icon" />
                ) : null}
              </div>
              <span className="category-label">{name}</span>
            </div>
          );
        })}
      </div>

      <button className="scroll-btn right" onClick={() => scroll("right")}>
        <ChevronRight size={20} color="rgba(255,255,255,0.95)" />
      </button>
    </div>
  );
};

export default CategoryBar;
