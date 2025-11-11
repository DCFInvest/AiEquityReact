import React, { useState } from "react";
import axios from "axios";

function ChatUI() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSend = async () => {
    if (!query) return;
    const userMsg = { sender: "user", text: query };
    setMessages([...messages, userMsg]);
    setQuery("");

    try {
      const res = await axios.post("http://localhost:5000/api/query", { query });
      const aiMsg = { sender: "ai", text: JSON.stringify(res.data, null, 2) };
      setMessages(prev => [...prev, userMsg, aiMsg]);
    } catch (err) {
      const aiMsg = { sender: "ai", text: "Error fetching data" };
      setMessages(prev => [...prev, userMsg, aiMsg]);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.sender}`}>
            {m.text}
          </div>
        ))}
      </div>
      <div className="input-box">
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Ask about a stock or sector..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}

export default ChatUI;
