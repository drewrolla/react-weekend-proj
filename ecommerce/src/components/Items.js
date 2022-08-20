import React, { Component } from 'react'

export default class Items extends Component {
  render() {
    const i = this.props.itemInfo
    return (
        <div className="card" style={{width: "18rem"}}>
        <img src={i.img_url} className="card-img-top" alt="..."/>
        <div className="card-body">
          <h5 className="card-title">{i.title}</h5>
          <p>{i.price}</p>
          <p>{i.author}</p>
          <p className="card-text">{i.caption}</p>
        </div>
      </div>
    )
  }
}
