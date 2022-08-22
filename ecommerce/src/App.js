import React, { Component } from 'react';
import { Routes, Route, BrowserRouter } from 'react-router-dom'
import Items from './components/Items';
import Nav from './components/Nav';
import Cart from './views/Cart';
import Home from './views/Home';
import Login from './views/Login';
import PostItem from './views/PostItem';
import Shop from './views/Shop';
import Signup from './views/Signup';
import SingleItem from './views/SingleItem';

export default class App extends Component {
  constructor() {
    super();
    this.state = {
      items: [],
      user: {}
    }
  };

  logMeIn = (user) => {
    this.setState({
      user: user
    })
  }

  render() {
    return (
      <BrowserRouter>
        <div>
          <Nav />
          <Routes>
            <Route path='/' element={<Home />} />
            <Route path='/login' element={<Login logMeIn={this.logMeIn}/>} />
            <Route path='/signup' element={<Signup />} />

            <Route path='/shop' element={<Shop user={this.state.user} />} />
            <Route path='/cart' element={<Cart user={this.state.user} />} />

            <Route path='/items' element={<Items user={this.state.user} />} />
            <Route path='/items/create' element={<PostItem user={this.state.user} />} />
            <Route path='/items/:itemsId' element={<SingleItem />} />
          </Routes>
        </div>
      </BrowserRouter>
    )
  }
}
