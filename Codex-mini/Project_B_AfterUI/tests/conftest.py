import pytest
import sys
import subprocess
import time
import os
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

@pytest.fixture(scope="session")
def server():
    env = os.environ.copy()
    proc = subprocess.Popen([sys.executable, "src/app.py"], cwd=root, env=env)
    time.sleep(2)
    try:
        yield
    finally:
        proc.terminate()
        proc.wait()
