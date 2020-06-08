import React from 'react';
import './App.css';
import { useState } from 'react';
import { useEffect } from 'react';
import socketIOClient from "socket.io-client";
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Button from 'react-bootstrap/Button';

import MessageScreen from './MessageScreen.js'

function App() {
  const [connected, setConnected] = useState(0);
  const [signedin, setSignedin] = useState(0);
  const [alias_list, setAliasList] = useState(0);
  const [waiter, setWaiter] = useState(0);
  const ENDPOINT = "http://127.0.0.1:5000";
  const socket = socketIOClient(ENDPOINT);
  
  useEffect(() => {
    fetch(
      '/connect', {
        method: 'post',
        headers: {'Content-Type':'application/json'}})
      .then(response => response.json())
      .then(data => {
        console.log(data)
    setConnected(data.connect);
    setSignedin(data.signedin);
    setAliasList(data.alias_list);

    if (!connected) {
      setWaiter(<img alt="Please wait!" className="centerContent" src="https://media.giphy.com/media/xT9DPldJHzZKtOnEn6/200w_d.gif"></img>);
    } else if (signedin === false) {
      setWaiter(<SigninDialogue></SigninDialogue>)
    }
  });
  }, []);

  class SigninDialogue extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        username: null,
        password: null
      };
      this._handleSubmit = this._handleSubmit.bind(this);
    }
  
    _handleSubmit = (e) => {
      fetch(
        '/connect', {
          method: 'post',
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify({
              user: this.state.username,
              pass: this.state.password
          })})
        .then(response => response.json()).then( d => {
          setConnected(true);
          setSignedin(d.signedin);
        });
    }
  
    render() {
      return (
        <div className="signinBox">
          <p className="title">fasemo</p>
          <InputGroup size="sm" className="mb-3">
            <FormControl onChange = {(event) => this.setState({username: event.target.value})} value={this.state.username} placeholder="Username"></FormControl>
            <FormControl type="password" onChange = {(event) => this.setState({password: event.target.value})} value={this.state.password} placeholder="Password"></FormControl>
          </InputGroup>
          <Button onClick={this._handleSubmit}>Sign In / Create Account</Button>
        </div>
      )
    }
  }

  return (
    <div className="App">
      <div className={"inFront frontPanel " + ((connected && signedin) ? 'offScreenTop' : 'onScreen')}>
        <p></p>
        {waiter}
        
      </div>

      {MessageScreen(socket)}
    </div>
  );
}

export default App;