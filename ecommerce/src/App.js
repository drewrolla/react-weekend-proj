import React, { Component } from 'react';
import { Routes, Route, BrowserRouter } from 'react-router-dom'
import Items from './components/Items';
import Nav from './components/Nav';
import Home from './views/Home';
import Login from './views/Login';
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
      user:user
    })
  };

  render() {
    return (
      <BrowserRouter>
        <div>
          <Nav />
          <Routes>
            <Route path='/' element={<Home />} />
            <Route path='/login' element={<Login />} />
            <Route path='/signup' element={<Signup />} />
            <Route path='/shop' element={<Shop />} />
            <Route path='/singleitem' element={<SingleItem />} />
            <Route path='/items' element={<Items />} />
          </Routes>
        </div>
      </BrowserRouter>
    )
  }
}
