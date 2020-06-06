import React from 'react';
import './App.css';
import { useState } from 'react';
import { useEffect } from 'react';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import ScrollArea from 'react-scrollbar';

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
        <img alt="" height="48" width="48" src={this.props.pic} className="profilePic" />
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
        <img alt="" height="48" width="48" src={this.props.pic} className="profilePic" />
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
        <img alt="" height="48" width="48" src={this.props.pic} className="profilePic" />
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
          <img alt="" height="48" width="48" src={this.props.pic} className="profilePic" />
        </div>
      </div>
    );
  }
}

class ConversationWindow extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            messagesEnd: null
        };
        this.boxRef  = React.createRef();
    }

    render() {
        let chat = '';

        if (this.props.chat) {
            chat = this.props.chat.map((mess) => {
            return (
                <ComponentMessage pic={"http://127.0.0.1:5005/profile_pics/" + mess.pic} text={mess.text}></ComponentMessage>
            );
        });
        }

        return (

            <ScrollArea speed={0.8} horizontal={false}>
                {chat}
                <div ref={this.boxRef}></div>
            </ScrollArea>
        )
    }
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

        fetch(
            '/post_message', {
            method: 'post',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({
                message: this.state.inputText
            })
        }).then(this.state.inputText = '');
    }
  }

  render() {

    return (
      <InputGroup size="sm" className="mb-3">
        <FormControl onChange = {(event) => this.setState({inputText: event.target.value})} value={this.state.inputText} placeholder="hOI!!" onKeyDown={this._handleKeyDown}></FormControl>
      </InputGroup>
    );
  }
}

function MessageScreen(socket) {
    const [currentChat, setCurrentChat] = useState(0);
  
    useEffect(() => {
        socket.on('refresh_thread', data => {
            setCurrentChat(JSON.parse(data));
        });
    }, []);

    return (
        <div className="flexboxHorz">
            <div className="leftPanel flexboxVert inFront">
                <div className="flexboxVertContent">
                    <ComponentThread text="CHAT 1" pic="http://127.0.0.1:5005/profile_pics/ac.png"></ComponentThread>
                    <ComponentThread text="CHAT 2" pic="http://127.0.0.1:5005/profile_pics/ac.png"></ComponentThread>
                    <ComponentThread text="CHAT 3" pic="http://127.0.0.1:5005/profile_pics/ac.png"></ComponentThread>
                </div>
                <SettingsBox></SettingsBox>
            </div>
            <div className="rightPanel flexboxVert">
                <ConversationWindow chat={currentChat}></ConversationWindow>
                <ComponentInputbox></ComponentInputbox>
            </div>
        </div>
    );
  }

export default MessageScreen;