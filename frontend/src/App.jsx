import React from "react";
import TrainForm from "./components/TrainForm";
import LoadModel from "./components/LoadModel";

export default function App() {
  return (
    <div className="min-h-screen p-6 max-w-5xl mx-auto space-y-12">
      <header className="text-center">
        <h1 className="text-3xl font-bold mb-2">🧠 LLM Fine-Tuner</h1>
        <p className="text-gray-600">Train and interact with your fine-tuned model</p>
      </header>
      <TrainForm />
      <LoadModel />
    </div>
  );
}
