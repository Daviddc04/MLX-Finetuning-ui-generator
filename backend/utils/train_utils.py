import os
import json
from datetime import datetime
import subprocess

DATA_DIR = "data"
ADAPTER_DIR = "adapters"

def save_jsonl_and_train(data):
    version = datetime.now().strftime("v_%Y%m%d_%H%M%S")
    version_path = os.path.join(ADAPTER_DIR, version)
    os.makedirs(version_path, exist_ok=True)

    # Save JSONL files
    for split in ['train', 'valid', 'test']:
        path = os.path.join(DATA_DIR, f"{split}.jsonl")
        with open(path, 'w') as f:
            for item in data[split]:
                f.write(json.dumps(item) + '\n')

    # Pass version path as argument to finetune script
    subprocess.run(["python", "finetune_and_fuse.py", version_path], check=True)
    return True, version

