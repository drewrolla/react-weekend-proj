import React, { Component } from 'react'

export default class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {
            message:false
        }
    }

    sendLoginInfo = async (e) => {
        e.preventDefault();

        const url = 'http://localhost:5000/api/login'
        const body = {
            username: e.target.username.value,
            password: e.target.password.value
        }

        const options = {
            method: "POST",
            headers: {
                "Content-Type": 'application/json'
            },
            body: JSON.stringify(body)
        }

        const res = await fetch(url, options);
        const data = await res.json();
        console.log(data)

        if (data.status === 'ok') {
            this.props.logMeIn(data.data)
        }

    };

    sendBasicAuth = async (e) => {
        e.preventDefault();
        const res = await fetch('http://localhost:5000/token', {
            method: "POST",
            headers: {Authorization: `Bearer ${btoa(e.target.username.value+":"+e.target.password.value)}`}
        });
        const data = await res.json();
        console.log(data)
        if (data.status === 'ok') {
            this.props.logMeIn(data.data)
            this.setState({message:true})
        }
    }


  render() {
    return (
        <form className='container col-4' onSubmit={(e) => { this.sendBasicAuth(e) }}>
            <div className="mb-3">
                <label htmlFor="username" className="form-label">Username</label>
                <input type="text" className="form-control" name='username' />
            </div>
            <div className="mb-3">
                <label htmlFor="password" className="form-label">Password</label>
                <input type="password" className="form-control" name='password' />
            </div>
            <button type="submit" className="btn btn-primary">Submit</button>
            <p>Don't have an account? Sign up <a href='/signup'>here!</a></p>
        </form>
    )
  }
}
