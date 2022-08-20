import React, { Component } from 'react'

export default class PostItem extends Component {
    sendCreate = async (e) => {
        e.preventDefault();
        const res = await fetch('http://localhost:5000/api/items/create', {
            method: "POST",
            headers: {
                Authorization: `Bearer ${this.props.user.token}`,
                "Content-Type": 'application/json'
            },
            body: JSON.stringify({
                title: e.target.title.value,
                price: e.target.price.value,
                description: e.target.description.value,
                imgUrl: e.target.imgUrl.value
            })
        });
        const data = await res.json();
        console.log(data)
    };

  render() {
    return (
        <form className='col-4' onSubmit={(e) => { this.sendCreate(e) }}>

            <div className="mb-3">
                <label className="form-label">Title</label>
                <input type="text" className="form-control" name='title' />
            </div>
            <div className="mb-3">
                <label className="form-label">Price</label>
                <input type="text" className="form-control" name='price' />
            </div>
            <div className="mb-3">
                <label className="form-label">Description</label>
                <input type="text" className="form-control" name='description' />
            </div>
            <div className="mb-3">
                <label className="form-label">Image URL</label>
                <input type="text" className="form-control" name='imgUrl' />
            </div>

            <button type="submit" className="btn btn-primary">Submit</button>
        </form>
    )
  }
}
