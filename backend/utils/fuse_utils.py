import os
import subprocess
import glob
from mlx_lm import load, generate

# Directory where adapter files are stored
ADAPTER_DIR = "./adapters"
FUSED_MODEL_DIR = "./fused_model"

# Cache for loaded fused model
MODEL_CACHE = {
    "model": None,
    "tokenizer": None
}

def list_adapters():
    """
    Lists all adapter directories (subdirs of ADAPTER_DIR that contain 'adapters.safetensors' file).
    Returns relative directory names like: ['v_20250701_133504', ...]
    """
    adapter_dirs = []
    for root, dirs, files in os.walk(ADAPTER_DIR):
        if "adapters.safetensors" in files and "adapter_config.json" in files:
            rel_path = os.path.relpath(root, ADAPTER_DIR)
            adapter_dirs.append(rel_path)

    return sorted(adapter_dirs)

def get_latest_adapter_dir():
    """
    Returns the latest adapter directory based on modification time of its 'adapters.safetensors' file.
    """
    adapter_dirs = list_adapters()
    if not adapter_dirs:
        raise FileNotFoundError("No adapter directories found with valid adapter files.")

    full_paths = [os.path.join(ADAPTER_DIR, d, "adapters.safetensors") for d in adapter_dirs]
    latest_file = max(full_paths, key=os.path.getmtime)
    latest_dir = os.path.dirname(latest_file)
    return latest_dir

def fuse_adapter(adapter_name=None):
    """
    Fuses the given adapter directory into the base model.
    adapter_name should be a relative directory name (like 'v_20250701_133504')
    If adapter_name is None, uses the latest adapter directory.
    """
    if adapter_name is None:
        # Get latest adapter directory
        adapter_dir = get_latest_adapter_dir()
    else:
        adapter_dir = os.path.join(ADAPTER_DIR, adapter_name)

    adapter_dir = os.path.normpath(adapter_dir)

    if not os.path.isdir(adapter_dir):
        raise FileNotFoundError(f"Adapter directory does not exist: {adapter_dir}")

    os.makedirs(FUSED_MODEL_DIR, exist_ok=True)
    save_path = FUSED_MODEL_DIR

    print(f"Fusing adapter from directory: {adapter_dir}")
    subprocess.run([
        "mlx_lm.fuse",
        "--model", "mlx-community/Mistral-7B-Instruct-v0.3-4bit",
        "--adapter-path", adapter_dir,
        "--save-path", save_path
    ], check=True)

    # Clear cached model
    MODEL_CACHE["model"] = None
    MODEL_CACHE["tokenizer"] = None

    return save_path


def load_fused_model():
    """
    Loads the fused model (only once).
    """
    if MODEL_CACHE["model"] is None or MODEL_CACHE["tokenizer"] is None:
        fused_model_path = FUSED_MODEL_DIR
        if not os.path.exists(fused_model_path):
            raise FileNotFoundError("Fused model not found. Please run fusion first.")

        print("Loading fused model for inference...")
        MODEL_CACHE["model"], MODEL_CACHE["tokenizer"] = load(fused_model_path)

def chat_with_model(prompt):
    """
    Generates a chat response using the loaded fused model.
    """
    load_fused_model()
    formatted_prompt = f"[INST] {prompt} [/INST]"
    response = generate(MODEL_CACHE["model"], MODEL_CACHE["tokenizer"], formatted_prompt, verbose=False)
    return response
