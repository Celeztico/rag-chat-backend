import os,time

BASE_DIR = os.getenv("DATA_DIR", "data")

def cleanup_uploads(days=7):
    now = time.time()
    cutoff = now - (days * 86400)

    root = f"{BASE_DIR}/uploads"

    for root_dir, dirs, files in os.walk(root):
        for file in files:
            path = os.path.join(root_dir, file)
            if os.path.getmtime(path) < cutoff:
                os.remove(path)