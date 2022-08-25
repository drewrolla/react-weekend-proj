import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom';
import Items from '../components/Items';

export default function Shop({addToCart}) {
    const [items, setItems] = useState([])

    const getItems = async () => {
        const res = await fetch('http://localhost:5000/api/items');
        const data = await res.json()
        setItems(data.items)
    }

    useEffect(()=>{
        getItems()
    }, [])

    const showItems = () => {
        return items.map(i=><Items key={i.id} addToCart={addToCart} item={i} />)
    }

  return (
    <div className='row'>
            {showItems()}
    </div>
  )
}
