import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import Items from '../components/Items';

export default function SingleItem({ user }) {
    const { itemId } = useParams()
    const [ item, setItem ] = useState({})

    const getSingleItem  = async () => {
        const res = await fetch(`http://localhost:5000/api/items/${itemId}`); // Flask app itemId
        const data = await res.json();
        if (data.status === 'ok'){
            setItem(data.item)
        }
    };

    useEffect(()=>{
        getSingleItem()
    }, [])

  return (
    <div>
        <Items itemInfo = {item}/>

    </div>
  )
}