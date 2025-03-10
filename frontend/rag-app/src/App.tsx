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

  const callDbpediaFunction = async (sparqlQuery: string): Promise<any> => {
    try {
      const response = await fetch('http://localhost:8000/dbpedia/querykg', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: sparqlQuery }),
      });
  
      if (!response.ok) {
        throw new Error('Error: Unable to process the DBpedia query.');
      }
  
      return await response.json();
    } catch (error) {
      throw new Error(
        `Error: Unable to connect to the DBpedia server. ${error instanceof Error ? error.message : ''}`
      );
    }
  };
  
  const callVectorSearchFunction = async (query: string): Promise<{ results: string[]; similarities: number[] }> => {
    try {
      const response = await fetch('http://localhost:8000/vector_search/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          query_text: query
        }),
      });
  
      if (!response.ok) {
        throw new Error('Error: Unable to process the vector search query.');
      }
  
      const data = await response.json();
      return {
        results: data.results.map((result: { text: string }) => result.text),
        similarities: data.results.map((result: { similarity: number }) => result.similarity),
      };
    } catch (error) {
      throw new Error(
        `Error: Unable to connect to the vector search server. ${error instanceof Error ? error.message : ''}`
      );
    }
  };

  const callLlmRespond = async (
    query: string,
    vectorResults: string[],
    kgContext: string
  ): Promise<string> => {
    try {
      const response = await fetch('http://localhost:8000/nlp/llm_response', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          vector_results: vectorResults,
          kg_context: kgContext,
        }),
      });
  
      if (!response.ok) {
        throw new Error('Error: Unable to process the LLM query.');
      }
            
      const data = await response.json();
      return data.response;

    } catch (error) {
      throw new Error(
        `Error: Unable to connect to the LLM server. ${error instanceof Error ? error.message : ''}`
      );
    }
  };
  
    
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (userMessage.trim() === '') return;
  
    // Add user's message to the chat
    const newMessage: Message = {
      text: userMessage,
      sender: 'user',
    };
  
    setMessages([...messages, newMessage]);
    setUserMessage('');
  
    try {
      console.log('User Input: ', userMessage);
      const startTime = performance.now();

      // Natural Language Processing
      const nlpStartTime = performance.now();
      const nlpData = await callNlpEndpoint(userMessage);
      const botMessage: Message = {
        text: `Tokens: ${nlpData.tokens.join(', ')}\nEntities: ${nlpData.entities.map((ent: Entity) => ent.text).join(', ')}\nIs Harmful: ${nlpData.is_harmful}\nSPARQL: ${nlpData.sparql_query}`,
        sender: 'bot',
      };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
      const nlpEndTime = performance.now();
      console.log(`NLP Time: ${nlpEndTime - nlpStartTime} ms`);
  
      // DBpedia Query
      const kgStartTime = performance.now();
      let dbpediaMessage: Message = {text: "", sender: "bot"}
      if (nlpData.sparql_query) {
        const dbpediaData = await callDbpediaFunction(nlpData.sparql_query);
        
        // Ensure dbpeida data has valid structure and text
        const firstBinding = dbpediaData?.results?.bindings?.[0];
        const abstractText = firstBinding?.abstract?.value || "No abstract available.";      

        dbpediaMessage = {
          text: `DBpedia Abstract: ${abstractText}`,
          sender: 'bot',
        };
        setMessages((prevMessages) => [...prevMessages, dbpediaMessage]);
      }
      const kgEndTime = performance.now();
      console.log(`DBpedia Time: ${kgEndTime - kgStartTime} ms`);
  
      // Vector Search
      const vectorSearchStartTime = performance.now();
      const vectorData = await callVectorSearchFunction(userMessage);
      const vectorMessage: Message = {
        text: `Vector Search Results:\n${vectorData.results.join('\n')}`,
        sender: 'bot',
      };
      setMessages((prevMessages) => [...prevMessages, vectorMessage]);
      const vectorSearchEndTime = performance.now();
      console.log(`Vector Search Time: ${vectorSearchEndTime - vectorSearchStartTime} ms`);  

      // Call LLM endpoint
      const llmStartTime = performance.now();
      const llmResponse = await callLlmRespond(userMessage, vectorData.results, dbpediaMessage.text)  
      const llmMessage: Message = {
        text: `LLM Response: ${llmResponse}`,
        sender: 'bot',
      };
  
      setMessages((prevMessages) => [...prevMessages, llmMessage]);
      const llmEndTime = performance.now();
      console.log(`LLM Response Time: ${llmEndTime - llmStartTime} ms`);

      const endTime = performance.now();
      console.log(`Total Time: ${endTime - startTime} ms`);
      if (endTime - startTime > 600) {
        console.log("Warning: The response time is too high. Please optimize the code.")
      }
  
    } catch (error) {
      const errorMessage: Message = {
        text: error instanceof Error ? error.message : 'An unknown error occurred.',
        sender: 'bot',
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
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