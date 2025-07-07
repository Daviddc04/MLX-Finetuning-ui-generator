import React, { useState, useEffect } from "react";
import axios from "axios";
import { LoaderCircle } from "lucide-react";

export default function LoadModel() {
  const [adapters, setAdapters] = useState([]);
  const [selected, setSelected] = useState("");
  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("");
  const [loading, setLoading] = useState(false);
  const [fusing, setFusing] = useState(false);

  useEffect(() => {
    axios.get('/api/adapters').then(res => setAdapters(res.data));
  }, []);

  const fuse = () => {
    setFusing(true);
    axios.post('/api/fuse', { adapter: selected })
      .then(() => alert("Model fused!"))
      .finally(() => setFusing(false));
  };

  const chat = () => {
    setLoading(true);
    axios.post('/api/chat', { prompt: message })
      .then(res => setReply(res.data.response))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  return (
    <section className="space-y-6">
      <h2 className="text-2xl font-semibold">💬 Load & Chat</h2>

      <div className="flex gap-4 items-center">
        <select onChange={(e) => setSelected(e.target.value)} className="min-w-[200px]">
          <option disabled selected>Select adapter</option>
          {adapters.map((a, i) => <option key={i}>{a}</option>)}
        </select>
        <button onClick={fuse} disabled={fusing}>
          {fusing ? <LoaderCircle className="animate-spin w-4 h-4 inline" /> : "Fuse Model"}
        </button>
      </div>

      <div className="bg-white p-4 rounded-xl shadow-md max-w-3xl mx-auto space-y-4">
        <div className="h-64 overflow-y-auto flex flex-col space-y-2">
          {message && <div className="chat-bubble chat-bubble-user self-end">{message}</div>}
          {reply && <div className="chat-bubble chat-bubble-bot self-start">{reply}</div>}
        </div>
        <div className="flex gap-2">
          <input
            className="flex-1"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message..."
          />
          <button onClick={chat} disabled={loading}>
            {loading ? <LoaderCircle className="animate-spin w-4 h-4 inline" /> : "Send"}
          </button>
        </div>
      </div>
    </section>
  );
}
