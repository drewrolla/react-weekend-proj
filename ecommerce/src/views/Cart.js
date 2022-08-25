import React from 'react'

export default function Cart({ cart, removeFromCart, user }) {

    const getUniqueCart = (cart) => {
        let uniqueCart = [];
        let ids = new Set();
        for (let item of cart) {
            if (!ids.has(item.id)) {
                uniqueCart.push(item)
                ids.add(item.id)
            }
        }
        return uniqueCart
    };
    const getQuantity = (searchItem, cart) => {
        let count = 0;
        for (let item of cart) {
            if (item.id === searchItem.id) {
                count++;
            }
        }
        return count
    };
    const getTotal = () => {
        const unique = getUniqueCart(cart)
        let total =0;
        for (let item of unique){
            total += getQuantity(item, cart) * item.price
        }
        return total.toFixed(2)
    }

    const removeFromCartAPI = async (item) => {
        const res = await fetch('http://localhost:5000/api/cart/remove', {
            method: "POST",
            headers: {
                Authorization: `Bearer ${user.token}`,
                "Content-Type": 'application/json'
            },
            body: JSON.stringify({itemId: item.id})
        });
        const data = await res.json();
        console.log(data)
    };

    const handleClick = (item) => {
        removeFromCart(item);
        if (user.token) {
            removeFromCartAPI(item)
        }
    };


    return cart.length === 0 ?
        (<h1>Your cart is empty.</h1>)
        :
        (
            <table class="table">
                <thead>
                    <tr>
                        <th scope="col">ID</th>
                        <th scope="col"></th>
                        <th scope="col">Name</th>
                        <th scope="col">Quantity</th>
                        <th scope="col">Price</th>
                        <th scope="col">Subtotal</th>
                        <th scope="col">Remove</th>
                    </tr>
                </thead>
                <tbody>

                    {getUniqueCart(cart).map(item => (
                        <tr key={item.id}>
                            <th scope="row">{item.id}</th>
                            <td><img style={{ width: '50px' }} src={item.img_url} alt='...'/></td>
                            <td>{item.item_name}</td>
                            <td>{getQuantity(item, cart)}</td>
                            <td>${item.price}</td>
                            <td>${(getQuantity(item, cart) * item.price).toFixed(2)}</td>
                            <td><button className='btn btn-danger' onClick={() => { handleClick(item);  }}>Remove</button></td>
                        </tr>
                    ))}

                </tbody>
                <tfoot>
                    <tr>
                        <th scope="col">Total</th>
                        <th scope="col"></th>
                        <th scope="col"></th>
                        <th scope="col"></th>
                        <th scope="col"></th>
                        <th scope="col">${getTotal()}</th>
                        <th scope="col"><button className='btn btn-success'>Checkout</button></th>
                    </tr>
                </tfoot>
            </table>
        )
}
