import React, { Component } from 'react'
import Items from '../components/Items';
import { Link } from 'react-router-dom';

export default class Shop extends Component {
    constructor(){
        super();
        this.state={
            items: []
        }
    }

    componentDidMount = async => {
        this.getItems()
    }

    getItems = async () => {
        const res = await fetch('http://localhost:5000/api/items'); // Flask link for showing items
        const data = await res.json();
        this.setState({items: data.items})
    }

    showItems = () => {
        return this.state.items.map(i=><Link key={i.id} to={`/items/${i.id}`}><Items itemInfo={i}/></Link>)
    }

  render() {
    return (
      <div>
        {this.showItems()}
      </div>
    )
  }
}
