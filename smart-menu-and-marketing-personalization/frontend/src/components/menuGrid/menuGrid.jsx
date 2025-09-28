import React, { useEffect, useState } from "react";
import axios from "axios";
import { Heart as HeartIcon } from "lucide-react";
import "./menuGrid.css";

// i put static images mapping bc the backend didnt provide the right images !! 
//so if theres an image in the beckend use it, otherwise fallback to static mapping
import pizzaVeg from "../../assets/pizza_vegitarienne.png";
import pizzaPepperoni from "../../assets/pizza_pepperoni.png";

import pizzaPepperoniTomato from "../../assets/pizza_margarit.png";
import pizzaMixedMeats from "../../assets/pizza_pepperoni_legumes.png";
import pizzaMerguez from "../../assets/pizza_mergaz.png"; 
import pizzaGroundMeat from "../../assets/pizza_viande_hachee.png"; 
import pizzaChicken from "../../assets/pizza_double_chicken.png"; 
import pizzaBBQChicken from "../../assets/pizza_poulet_bbq_sauce.png"; 
import pizzaVegChicken from "../../assets/pizza_legumes_poulet.png"; 
import pizzaMushroom from "../../assets/pizza_mushroom.png"; 
import gelatoImage from "../../assets/7.png"; //gelato image ( i know it not gelato :D )

export default function MenuGrid({ selectedCategory, addToCart = () => {} }) {
  const [menuItems, setMenuItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // favorites persisted locally
  const [favorites, setFavorites] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem("fav_items") || "[]");
    } catch {
      return [];
    }
  });

  const toggleFavorite = (id) => {
    setFavorites((prev) => {
      const exists = prev.includes(id);
      const next = exists ? prev.filter((i) => i !== id) : [...prev, id];
      try {
        localStorage.setItem("fav_items", JSON.stringify(next));
      } catch { /* empty */ }
      return next;
    });
  };

  const fetchMenu = () => {
    setLoading(true);
    setError(null);
    axios
      .get("http://localhost:8000/api/menu-items/")
      .then((response) => {
        setMenuItems(response.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching menu items:", err);
        setError("Failed to load menu.");
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchMenu();
  }, []);

  // map (CategoryBar) -> backend category values
  const categoryMap = {
    "Pizzas": "Pizza",
    "Salads": "Salad",
    "Desserts": "Dessert",
    "Drinks": "Cold Drink",
    "Hot Drinks": "Hot Drink",
    "Gelato": "Gelato",
    "Bakery": "Bakery",
  };

  // Show all items  for "For you" or "Pizzas" for demo only, it should change based on the user preferences
  const showAll =
    selectedCategory === "For you" || selectedCategory === "Pizzas";

  const backendCategory = categoryMap[selectedCategory] || selectedCategory;

  const filteredItems = showAll
    ? menuItems
    : menuItems.filter((item) => item.category === backendCategory);

  // static image map 
  const imageMap = {
    "mixed meats": pizzaMixedMeats,
    "merguez": pizzaMerguez,
    "pepperoni": pizzaPepperoni,
    "pepperoni & tomatoes": pizzaPepperoniTomato,
    "pepperoni & tomato": pizzaPepperoniTomato,
    "ground meat": pizzaGroundMeat,
    "bbq": pizzaBBQChicken,
    "barbecue chicken": pizzaBBQChicken,
    "chicken": pizzaChicken,
    "vegetables & chicken": pizzaVegChicken,
    "vegetables and chicken": pizzaVegChicken,
    "veg & chicken": pizzaVegChicken,
    "mushroom": pizzaMushroom,
    "gelato": gelatoImage,
    // fallback pizzas map 
    "default_pizza": pizzaVeg,
  };

  // fallback
  const getImageForItem = (item) => {

    if (item.image) return item.image;

    const name = (item.name && (item.name.en || item.name)) || "";
    const lower = String(name).toLowerCase().trim();


    if (imageMap[lower]) return imageMap[lower];


    for (const key of Object.keys(imageMap)) {
      if (key === "default_pizza") continue;
      if (lower.includes(key)) return imageMap[key];
    }

    // if category is Gelato, use gelato image -- FOR DEMO ONLY 
    if (String(item.category).toLowerCase() === "gelato") return gelatoImage;

    // else fallback
    return imageMap["default_pizza"];
  };

  if (loading)
    return (
      <div className="menu-loading" aria-busy="true">
        <div className="loading-box">
          <div className="spinner" role="img" aria-label="Loading"></div>
          <div className="loading-text">
            <strong>Loading menu...</strong>
            <div className="loading-sub">Fetching fresh items for you :3 </div>
          </div>
        </div>
      </div>
    );

  if (error)
    return (
      <div className="menu-error">
        <div className="error-box" role="alert">
          <svg
            className="error-icon"
            viewBox="0 0 24 24"
            width="36"
            height="36"
            aria-hidden
          >
            <circle cx="12" cy="12" r="10" fill="#fee2e2"></circle>
            <path
              d="M12 7v6"
              stroke="#ef4444"
              strokeWidth="1.6"
              strokeLinecap="round"
              strokeLinejoin="round"
            ></path>
            <path
              d="M12 16h.01"
              stroke="#ef4444"
              strokeWidth="1.6"
              strokeLinecap="round"
              strokeLinejoin="round"
            ></path>
          </svg>
          <div className="error-text">
            <strong>Could not load menu</strong>
            <div className="error-sub">Check your connection or try again.</div>
            <div className="error-actions">
              <button className="retry-btn" onClick={fetchMenu}>
                Retry
              </button>
            </div>
          </div>
        </div>
      </div>
    );

  return (
    <section className="menu-section">
      <header className="menu-header">
        <h2>Our Menu</h2>
        <p>Choose your favorite</p>
      </header>

      <div className="menu-grid">
        {filteredItems.map((item) => {
          const imgSrc = getImageForItem(item);
          const price = Number(item.price || 0).toFixed(2);

          return (
            <article key={item.item_id} className="menu-card">
              {/* favorite heart */}
              <button
                className={`fav-btn ${
                  favorites.includes(item.item_id) ? "active" : ""
                }`}
                onClick={(e) => {
                  e.stopPropagation();
                  toggleFavorite(item.item_id);
                }}
                aria-pressed={favorites.includes(item.item_id)}
                title={
                  favorites.includes(item.item_id)
                    ? "Remove favorite"
                    : "Add to favorites"
                }
              >
                <HeartIcon />
              </button>

              <img
                src={imgSrc}
                alt={(item.name && (item.name.en || item.name)) || "menu item"}
                className="menu-card-image"
                onError={(e) => {
                  // if a backend URL 404s
                  e.currentTarget.src = pizzaVeg;
                }}
              />

              <div className="menu-card-body">
                <h3>{item.name?.en || item.name}</h3>
                <p className="menu-desc">{item.description?.en || ""}</p>
                <p className="menu-price">${price}</p>
                <button
                  onClick={() => addToCart(item)}
                  className="add-btn"
                  aria-label={`Add ${item.name?.en || item.name} to cart`}
                >
                  Add to Cart
                </button>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}
