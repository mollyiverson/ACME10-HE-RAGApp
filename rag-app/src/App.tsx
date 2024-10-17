import React, { useState, FormEvent } from 'react';
import './App.css';

type Message = {
  text: string;
  sender: 'user' | 'bot';
};

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [userMessage, setUserMessage] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (userMessage.trim() === '') return;

    const newMessage: Message = {
      text: userMessage,
      sender: 'user',
    };

    setMessages([...messages, newMessage]);
    setUserMessage('');

    // Basic response from the RAG model
    setTimeout(() => {
      const ragResponse: Message = {
        text: 'RAG Model gives appropriate response',
        sender: 'bot',
      };
      setMessages((prevMessages) => [...prevMessages, ragResponse]);
    }, 1000);
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      {/* Chat box container */}
      <div className="flex flex-col w-full max-w-lg h-[600px] bg-white shadow-lg rounded-lg overflow-hidden">
        {/* Chat window */}
        <div className="flex-grow p-4 overflow-y-auto bg-gray-50">
          <div className="space-y-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`p-3 rounded-lg shadow ${
                  message.sender === 'user'
                    ? 'bg-blue-500 text-white self-end'
                    : 'bg-gray-300 text-gray-800 self-start'
                }`}
              >
                {message.text}
              </div>
            ))}
          </div>
        </div>

        {/* Input box */}
        <form onSubmit={handleSubmit} className="p-4 bg-gray-200 border-t border-gray-300">
          <div className="flex">
            <input
              type="text"
              value={userMessage}
              onChange={(e) => setUserMessage(e.target.value)}
              placeholder="Type your message..."
              className="flex-grow p-3 border border-gray-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="submit"
              className="ml-4 px-6 py-3 bg-blue-500 text-white rounded-lg shadow hover:bg-blue-600 transition duration-200"
            >
              Send
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;
