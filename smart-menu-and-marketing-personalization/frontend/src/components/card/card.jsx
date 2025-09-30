import React from 'react'
import './card.css'
import { IoAddOutline } from "react-icons/io5";


const Card = () => {
  return (
    <div className='menuContainer'>
      <article className='  productCard'>
            <div className='productCard-bg'></div>
            
            
            <h3 className='productCard-title'>Coffee</h3>
            <span className='productCard-subtitle'>Hot Beverage</span>
            <h3 className='productCard-price'>150 DA</h3>
            <button className='productCard-button'>
                <IoAddOutline />
            </button>

        </article>
        <article className='  productCard'>
            <div className='productCard-bg'></div>
            
            
            <h3 className='productCard-title'>Mushroom Pizza</h3>
            <span className='productCard-subtitle'>Pizza</span>
            <h3 className='productCard-price'>350 DA</h3>
            <button className='productCard-button'>
                <IoAddOutline />
            </button>

        </article>
    </div>
  )
}

export default Card;