import React from 'react';
import './App.css';
import { useState } from 'react';
import { useEffect } from 'react';

function App() {
  const [currentChat, setCurrentChat] = useState(0);

  useEffect(() => {
    fetch('/refresh_thread').then(res => res.json()).then(data => {
      setCurrentChat(data.message);
    });
  }, []);

  return (
    <div className="flexboxHorz">
      <div className="leftPanel flexboxVert">
        <ComponentMessage text="Is this working?" pic="http://127.0.0.1:5005/profile_pics/ac.png"></ComponentMessage>
      </div>
      {ConversationWindow(currentChat)};
    </div>
  );
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
        <div className="profilePic">
          <img height="48" width="48" src={this.props.pic} className="myProfPic" />
        </div>
        <div>
          <div>
            {this.props.text}
          </div>
        </div>
      </div>
    );
  }
}

function ConversationWindow(currentChat) {
  let chat = null;

  if (currentChat) {
    chat = currentChat.map((pic) => {
      return (
        <ComponentMessage pic={pic.pic} text={pic.text}></ComponentMessage>
      ) 
   });
  }

  return (
    <div className="rightPanel flexboxVert">
      {chat}
    </div>
  );
}

export default App;