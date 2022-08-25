import React, { useState, useEffect } from 'react'
import Items from '../components/Items';
import { useParams, Link } from 'react-router-dom'

export default function Singleitem({ user }) {
    const { itemId }  = useParams()
    const [ item, setItem ] = useState({})

    const getSingleItem = async () => {
        const res = await fetch(`http://localhost:5000/api/items/${itemId}`)
        const data = await res.json();
        if (data.status === 'ok'){
            setItem(data.item)
        }
    }

    useEffect(()=>{
        getSingleItem()
    }, [])

  return (
    <div>
        <Items item={item} />
    </div>
  )
}
