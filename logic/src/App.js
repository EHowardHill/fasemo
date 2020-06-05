import React from 'react';
import './App.css';
import { useState } from 'react';
import { useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';

function App() {
  const [currentChat, setCurrentChat] = useState(0);
  const refreshRate = 50;

  useEffect(() => {
    setInterval(function() {
      fetch(
        '/refresh_thread', {
        method: 'post',
        headers: {'Content-Type':'application/json'}
      }
      ).then(res => res.json()).then(data => {
        setCurrentChat(data.message);
      });
    }, refreshRate);
  }, []);

  return (
    <div className="App">
      <div className="flexboxHorz">
        <div className="leftPanel flexboxVert inFront">
          <div className="flexboxVertContent">
            <ComponentThread text="CHAT 1" pic="http://127.0.0.1:5005/profile_pics/ac.png"></ComponentThread>
            <ComponentThread text="CHAT 2" pic="http://127.0.0.1:5005/profile_pics/ac.png"></ComponentThread>
            <ComponentThread text="CHAT 3" pic="http://127.0.0.1:5005/profile_pics/ac.png"></ComponentThread>
          </div>
          <SettingsBox></SettingsBox>
        </div>
        {ConversationWindow(currentChat)}
      </div>
    </div>
  );
}

class ComponentThread extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      text: null,
      pic: null
    };
  }

  render() {
    return (
      <div className="thread">
        <img height="48" width="48" src={this.props.pic} className="profilePic" />
        <div>
          {this.props.text}
        </div>
      </div>
    );
  }
}

class ComponentMessage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      text: null,
      pic: null
    };
  }

  render() {
    return (
      <div className="message">
        <img height="48" width="48" src={this.props.pic} className="profilePic" />
        <div>
          {this.props.text}
        </div>
      </div>
    );
  }
}

class ComponentInputbox extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      text: null
    };
  }

  render() {
    return (
      <div className="inputBox">
        <img height="48" width="48" src={this.props.pic} className="profilePic" />
        <InputBox></InputBox>
      </div>
    );
  }
}

class SettingsBox extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      text: null
    };
  }

  render() {
    return (
      <div className="inputBox">
        <div className="profilePic">
          <img height="48" width="48" src={this.props.pic} className="profilePic" />
        </div>
      </div>
    );
  }
}

function ConversationWindow(currentChat) {
  let chat = null;

  if (currentChat) {
    chat = currentChat.map((mess) => {
      return (
        <ComponentMessage pic={mess.pic} text={mess.text}></ComponentMessage>
      ) 
   });
  }

  return (
    <div className="rightPanel flexboxVert">
      <div className="flexboxVertContent">
        {chat}
      </div>
      <ComponentInputbox></ComponentInputbox>
    </div>
  );
}

class InputBox extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      inputText: ''
    };
    this._handleKeyDown = this._handleKeyDown.bind(this);
  }

  _handleKeyDown = (e) => {
    if (e.key === 'Enter') {

      // Take care of the backend
      fetch(
        '/post_message', {
          method: 'post',
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify({
            message: this.state.inputText
          })
      });
    }
  }

  render() {

    return (
      <InputGroup size="sm" className="mb-3">
        <FormControl onChange = {(event) => this.setState({inputText: event.target.value})} placeholder="hOI!!" onKeyDown={this._handleKeyDown}></FormControl>
      </InputGroup>
    );
  }
}

export default App;