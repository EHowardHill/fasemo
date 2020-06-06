import React from 'react';
import './App.css';
import { useState } from 'react';
import { useEffect } from 'react';
import socketIOClient from "socket.io-client";

import MessageScreen from './MessageScreen.js'

function App() {
  const [connected, setConnected] = useState(0);
  const [signedin, setSignedin] = useState(0);
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

    if (connected === false) {
      setWaiter(<img alt="" className="centerContent" src="https://media.giphy.com/media/xT9DPldJHzZKtOnEn6/200w_d.gif"></img>);
    } else if (signedin === false) {
      setWaiter(<p className="centerContent" style="color: black;">ya need ta sign in</p>)
    }
  });
  }, []);

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