import subprocess
import sys
import os

def install_requirements():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def run_application():
    script_path = os.path.join("src", "media_map.py")
    subprocess.check_call([sys.executable, script_path])

if __name__ == "__main__":
    install_requirements()
    run_application()
