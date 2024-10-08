import sys
import os
import uvicorn

base_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(base_dir, "..", "app"))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
