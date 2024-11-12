import React, { useState, FormEvent } from 'react';
import './App.css';

type Message = {
  text: string;
  sender: 'user' | 'bot';
};

type Entity = {
  text: string;
  label: string;
};

type NlpData = {
  tokens: string[];
  entities: Entity[];
  is_harmful: boolean;
  sparql_query: string;
};

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [userMessage, setUserMessage] = useState('');

  const callNlpEndpoint = async (query: string): Promise<NlpData> => {
    try {
      const response = await fetch('http://localhost:8000/nlp/process_query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (response.ok) {
        const data = await response.json();
        return data;
      } else {
        throw new Error('Error: Unable to process the query.');
      }
    } catch (error) {
      if (error instanceof Error) {
        throw new Error('Error: Unable to connect to the server.');
      } else {
        throw error;
      }
    }
  };

  const callDbpediaFunction = async (sparqlQuery: string) => {
    try {
      const response = await fetch('http://localhost:8000/dbpedia/querykg', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: sparqlQuery }),
      });

      if (response.ok) {
        const data = await response.json();
        return data;
      } else {
        throw new Error('Error: Unable to process the DBpedia query.');
      }
    } catch (error) {
      if (error instanceof Error) {
        throw new Error('Error: Unable to connect to the DBpedia server.');
      } else {
        throw error;
      }
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (userMessage.trim() === '') return;

    const newMessage: Message = {
      text: userMessage,
      sender: 'user',
    };

    setMessages([...messages, newMessage]);
    setUserMessage('');

    try {
      const nlpData = await callNlpEndpoint(userMessage);
      const botMessage: Message = {
        text: `Tokens: ${nlpData.tokens.join(', ')}\nEntities: ${nlpData.entities.map((ent: Entity) => ent.text).join(', ')}\nIs Harmful: ${nlpData.is_harmful}\nSPARQL: ${nlpData.sparql_query}`,
        sender: 'bot',
      };
      setMessages((prevMessages) => [...prevMessages, botMessage]);

      if (nlpData.sparql_query) {
        const dbpediaData = await callDbpediaFunction(nlpData.sparql_query);
        const dbpediaMessage: Message = {
          text: `DBpedia Abstract: ${dbpediaData.results.bindings[0].abstract.value}`,
          sender: 'bot',
        };
        setMessages((prevMessages) => [...prevMessages, dbpediaMessage]);
      }

    } catch (error) {
      if (error instanceof Error) {
        const errorMessage: Message = {
          text: error.message,
          sender: 'bot',
        };
        setMessages((prevMessages) => [...prevMessages, errorMessage]);
      } else {
        const errorMessage: Message = {
          text: 'An unknown error occurred.',
          sender: 'bot',
        };
        setMessages((prevMessages) => [...prevMessages, errorMessage]);
      }
    }
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
                className={`p-3 rounded-lg shadow ${message.sender === 'user'
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