import React, { Component } from 'react'
import { Link } from 'react-router-dom';
import Items from '../components/Items';

export default class Cart extends Component {
  constructor() {
    super();
    this.state = {
      cart: []
    }
  }

  componentDidMount = async () => {
    this.getCart()
  }

  getCart = async () => {
    const res = await fetch('http://localhost:5000/api/cart');
    const data = await res.json();
    this.setState({cart: data.cart})
  }

  showCart = () => {
    return this.state.cart.map(i=><Link key={i.id} to={`/items/${i.id}`}><Items itemInfo={i}/></Link>)
  }

  render() {
    return (
      <div>Cart</div>
    )
  }
}