import os, subprocess, sys, time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
venv_dir = os.path.join(BASE_DIR, "venv", "Scripts" if os.name == "nt" else "bin")
python_exe = os.path.join(venv_dir, "python")

proc = subprocess.Popen([python_exe, "-m", "streamlit", "run", os.path.join(BASE_DIR, "Home.py")])

try:
    proc.wait()
except KeyboardInterrupt:
    proc.terminate()
