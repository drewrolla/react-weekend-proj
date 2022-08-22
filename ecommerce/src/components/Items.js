import React, { Component } from 'react'

export default class Items extends Component {
  render() {
    const i = this.props.itemInfo
    return (
        <div className="card" style={{width: "18rem"}}>
        <img src={i.img_url} className="card-img-top" alt="..."/>
        <div className="card-body">
          <p className="card-title">{i.title}</p>
          <p className='items'>${i.price}</p>
          <p>{i.author}</p>
          <p className="items">{i.description}</p>
          <button className='btn btn-primary'>Add to cart</button>
        </div>
      </div>
    )
  }
}
