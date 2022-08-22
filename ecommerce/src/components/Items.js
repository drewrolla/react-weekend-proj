import React, { Component } from 'react'
import { Link } from 'react-router-dom';

export default class Items extends Component {
  constructor(props) {
    super(props);
    this.state = {
      message:false
    }
  }



  addToCart = async (e) => {
    e.preventDefault();
    const res = await fetch('http://localhost:5000/api/cart/add', {
      method: "POST",
      headers: {
        Authorization: `Bearer ${this.props.user.token}`,
        "Content-Type": 'application/json'
      },
      body: JSON.stringify({
        title: this.props.itemInfo.title
      })
    });
    const data = await res.json();
    console.log(data)
    this.setState({message: true})
  }

  render() {
    const i = this.props.itemInfo
    return (
        <div className="card" style={{width: "18rem"}}>
        <img src={i.img_url} className="card-img-top" alt="..."/>
        <div className="card-body">
          <p className="card-title">{i.title}</p>
          <p className='items'>${i.price}</p>
          <p className="items">{i.description}</p>
          <Link key={i.id} to={`/items/${i.id}`} className='btn btn-secondary'>View</Link>
          <button onClick={(e)=>{ this.addToCart(e) }} className='btn btn-primary'>Add</button>
        </div>
      </div>
    )
  }
}
