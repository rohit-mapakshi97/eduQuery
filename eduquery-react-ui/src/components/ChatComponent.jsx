import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatComponent.css';

const backendURL = import.meta.env.VITE_BACKEND_URL;

const ChatComponent = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "👋 Hi! I'm EduQuery's assistant. How can I help you today?"
    }
  ]);
  const [userInput, setUserInput] = useState('');
  const chatBodyRef = useRef(null);

  useEffect(() => {
    if (chatBodyRef.current) {
      chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = async () => {
    if (userInput.trim() === '') return;

    const userMessage = { role: 'user', content: userInput };
    setMessages(prev => [...prev, userMessage]);
    setUserInput('');

    try {
      const response = await axios.post(`${backendURL}/message`, { prompt: userInput });
      const assistantMessage = {
        role: 'assistant',
        content: response.data.assistant_message
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error(error);
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: "Oops! Something went wrong. Please try again." }
      ]);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
      e.preventDefault();
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-body" ref={chatBodyRef}>
        {messages.map((msg, idx) => (
          <div key={idx} className={`chat-message ${msg.role}`}>
            <span className="avatar">
              {msg.role === 'user' ? '🧑‍💻' : '🤖'}
            </span>
            <span className="message-content">{msg.content}</span>
          </div>
        ))}
      </div>

      <div className="chat-input-container">
        <input
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message here..."
        />
        <button onClick={sendMessage}>➤</button>
      </div>
    </div>
  );
};

export default ChatComponent;
