import sys
import subprocess
import os

BASE_MODEL = "mlx-community/Mistral-7B-Instruct-v0.3-4bit"
DATA_DIR = "./data"

if len(sys.argv) < 2:
    raise ValueError("Expected adapter save path as argument")

ADAPTER_SAVE_PATH = sys.argv[1]  # This is now like ./adapters/v_20250613_123456

train_data_path = os.path.join(DATA_DIR, "train.jsonl")
with open(train_data_path, "r") as f:
    train_lines = f.readlines()
train_size = len(train_lines)
batch_size = min(train_size, 8)

import shutil

def finetune():
    print("Starting LoRA fine-tuning via subprocess...")
    command = [
        "mlx_lm.lora",
        "--model", BASE_MODEL,
        "--train",
        "--data", DATA_DIR,
        "--iters", "100",
        "--batch-size", str(batch_size),
        "--learning-rate", "1e-5",
    ]
    subprocess.run(command, check=True)

    # Move adapter.safetensors to versioned adapter folder
    #default_adapter_path = "adapter.safetensors"
    #if os.path.exists(default_adapter_path):
    #    shutil.move(default_adapter_path, os.path.join(ADAPTER_SAVE_PATH, "adapter.safetensors"))
    #    print(f"Adapter moved to: {os.path.join(ADAPTER_SAVE_PATH, 'adapter.safetensors')}")
    #else:
    #    print("Adapter file was not created. But training still works dw ")
    os.makedirs(ADAPTER_SAVE_PATH, exist_ok=True)

    # Move all .safetensors from adapters/ to the versioned folder
    adapter_output_dir = "adapters"
    for file in os.listdir(adapter_output_dir):
        if file.endswith(".safetensors"):
            full_path = os.path.join(adapter_output_dir, file)
            dest_path = os.path.join(ADAPTER_SAVE_PATH, file)
            print(f"Moving {file} to {dest_path}")
            os.rename(full_path, dest_path)
            print(f" All adapters moved to versioned path: {ADAPTER_SAVE_PATH}")
        elif file.endswith(".json"):
            full_path = os.path.join(adapter_output_dir, file)
            dest_path = os.path.join(ADAPTER_SAVE_PATH, file)
            print(f"Moving {file} to {dest_path}")
            os.rename(full_path, dest_path)


if __name__ == "__main__":
    finetune()
