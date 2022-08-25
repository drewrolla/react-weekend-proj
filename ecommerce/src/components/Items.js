import React from 'react'

export default function Items({ item, addToCart }) {
  return (
    <div className="card" style={{width: "18rem"}}>
        <img src={item.img_url} className="card-img-top" alt="..." />
        <div className="card-body">
            <h5 className="card-title">{item.items_name}</h5>
            <p className="card-text">{item.price}</p>
            <p className="card-text">{item.description}</p>
            <button onClick={()=>{addToCart(item)}} className="btn btn-primary">Add to Cart</button>
        </div>
    </div>
  )
}
