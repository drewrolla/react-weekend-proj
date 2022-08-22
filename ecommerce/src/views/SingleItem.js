import React, { useState, useEffect } from 'react'
import { Link, useParams } from 'react-router-dom'
import Items from '../components/Items';

export default function SingleItem({ user }) {
    const { itemsId } = useParams()
    const [ item, setItem ] = useState({})

    const getSingleItem  = async () => {
        const res = await fetch(`http://localhost:5000/api/items/${itemsId}`); // Flask app itemsId
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

        <Link to={`/items/${itemsId}`}>
        </Link>

    </div>
  )
}
