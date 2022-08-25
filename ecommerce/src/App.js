import React, { useState, useEffect } from 'react';
import { Routes, Route, BrowserRouter } from 'react-router-dom'
import Nav from './components/Nav';
import Cart from './views/Cart';
import Home from './views/Home';
import Login from './views/Login';
import Shop from './views/Shop';
import Signup from './views/Signup';
import Singleitem from './views/Singleitem';

export default function App() {
  // constructor() {
  //   super();
  //   this.state = {
  //     items: [],
  //     user: {},
  //     cart: []
  //   }
  // };
  const getUserFromLocalStorage = () => {
    const foundUser = localStorage.getItem('user')
    if (foundUser){
      return JSON.parse(foundUser)
    }
    return {}
  };

  const [user, setUser] = useState(getUserFromLocalStorage())
  const [cart, setCart] = useState([])

  // logMeIn = (user) => {
  //   this.setState({
  //     user: user
  //   })
  // }

  const logMeIn = (user) => {
    setUser(user)
    localStorage.setItem('user', JSON.stringify(user))
  }

  const logMeOut = () => {
    setUser({})
    localStorage.removeItem('user')
  }

  const addToCart = (item) => {
    setCart([...cart, item])
  }

  const removeFromCart = (item) => {
    const newCart = [...cart]
    for (let i=cart.length-1; i>=0; i--){
      if (item.id == cart[i].id){
        newCart.splice(i, 1)
        break
      }
    }
    setCart(newCart)
  }
  
  const getCart = async (user) => {
    if (user.token){
      const res = await fetch('http://localhost:5000/api/cart', {
        method: "GET",
        headers: {Authorization: `Bearer ${user.token}`}
      });
      const data = await res.json();
      console.log(data)
      if (data.status==='ok'){
        setCart(data.cart)
      }
      else{
       setCart([]) 
      }
    }
    else{
      setCart([]) 
    }
  };

  useEffect(()=>{
    getCart(user)
  }, [user])

    return (
      <BrowserRouter>
        <div>
        <Nav user={user} cart={cart} logMeOut={logMeOut}/>

          <Routes>
            <Route path='/' element={<Home />} />
            <Route path='/login' element={<Login logMeIn={logMeIn} />} />
            <Route path='/signup' element={<Signup />} />

            <Route path='/shop' element={<Shop addToCart={addToCart} user={user}/>} />
            <Route path='/shop/:itemId' element={<Singleitem />} />
            <Route path='/cart' element={<Cart cart={cart} removeFromCart={removeFromCart} user={user}/>} />

          </Routes>
        </div>
      </BrowserRouter>
    )
  }
