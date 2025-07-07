# MLX LoRA Fine-Tuning UI

This is a full-stack application designed to simplify LoRA fine-tuning for MLX-supported large language models (LLMs). It provides a user-friendly web interface to fine-tune models, track adapter versions, and manage training configurations, all without needing deep command-line expertise.

## Features:

- Automates creation of Finetuning dependencies -> Train.json, Valid.json, Test.json
- Automates finetuning of the Model once you have filled out your training parameters
- Stores adapter version in timestamped folders so you can simply fuse any finetuned weights
to the base model and use that finetuned model.
- Automates fusing the adapter weights with the base model
- Provides a Chat where you can try out your finetuned LLM model.

**🎥 Watch the demo (Very simple example):** https://www.loom.com/share/528e8e2b101d4f3fa6a2acf85e961c2d?sid=d6cae6f7-b0b4-4686-b336-dc9133a72bbb

## Instructions:

# Setting up Backend:

cd backend
python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt

Or if you have conda installed you can do this below

cd backend
conda create -n new_env python=3.12
conda activate new_env
pip install -r requirements.txt

# Setting up Frontend:

cd frontend
npm install

# TO RUN : 
# cd backend -> python app.py 
# cd frontend -> npm start

# Features Coming:
- Docker Support
- A describe chat for the agent which will allow you to create the personality of the finetuned AI


