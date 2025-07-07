from flask import Flask, request, jsonify
from utils.train_utils import save_jsonl_and_train
from utils.fuse_utils import list_adapters, fuse_adapter, chat_with_model, ADAPTER_DIR
import os
app = Flask(__name__)

@app.route('/api/train', methods=['POST'])
def train():
    data = request.json
    success, version = save_jsonl_and_train(data)
    return jsonify({"success": success, "version": version})

@app.route('/api/adapters', methods=['GET'])
def adapters():
    return jsonify(list_adapters())

    
@app.route("/api/fuse", methods=["POST"])
def fuse():
    data = request.get_json()
    adapter_name = data.get("adapter_name", None)

    if adapter_name and adapter_name.startswith(ADAPTER_DIR):

        adapter_name = os.path.relpath(adapter_name, ADAPTER_DIR)

    try:
        fused_path = fuse_adapter(adapter_name)
        return jsonify({"status": "success", "fused_model_path": fused_path})
    except Exception as e:
        print(f"Fusion error: {e}")  
        return jsonify({"status": "error", "message": str(e)}), 500




@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        if not prompt:
            return jsonify({'error': 'Prompt is required.'}), 400

        response = chat_with_model(prompt)
        return jsonify({'response': response})

    except Exception as e:
        print(f"Chat API error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
