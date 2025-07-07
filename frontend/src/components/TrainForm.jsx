import React, { useState } from "react";
import axios from "axios";

export default function TrainForm() {
  const [train, setTrain] = useState([{ prompt: "", completion: "" }]);
  const [valid, setValid] = useState([{ prompt: "", completion: "" }]);
  const [test, setTest] = useState([{ prompt: "", completion: "" }]);

  const handleChange = (e, i, section) => {
    const data = section === 'train' ? [...train] : section === 'valid' ? [...valid] : [...test];
    data[i][e.target.name] = e.target.value;
    section === 'train' ? setTrain(data) : section === 'valid' ? setValid(data) : setTest(data);
  };

  const addEntry = (section) => {
    const entry = { prompt: "", completion: "" };
    section === 'train' ? setTrain([...train, entry])
      : section === 'valid' ? setValid([...valid, entry])
      : setTest([...test, entry]);
  };

  const trainModel = async () => {
    await axios.post('/api/train', { train, valid, test });
    alert("Training started!");
  };

  return (
    <section>
      <h2 className="text-2xl font-semibold mb-4">🛠 Training Data</h2>
      {["train", "valid", "test"].map((section) => (
        <div key={section} className="mb-6">
          <h4 className="text-lg font-medium mb-2">{section.toUpperCase()}</h4>
          {(section === 'train' ? train : section === 'valid' ? valid : test).map((entry, i) => (
            <div key={i} className="flex gap-2 mb-2">
              <input
                className="flex-1"
                name="prompt"
                value={entry.prompt}
                onChange={(e) => handleChange(e, i, section)}
                placeholder="Prompt"
              />
              <input
                className="flex-1"
                name="completion"
                value={entry.completion}
                onChange={(e) => handleChange(e, i, section)}
                placeholder="Completion"
              />
            </div>
          ))}
          <button onClick={() => addEntry(section)}>Add Entry</button>
        </div>
      ))}
      <button onClick={trainModel}>Train Model</button>
    </section>
  );
}
