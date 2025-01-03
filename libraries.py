import subprocess
import sys

def install(package):
    """
    Installs a Python package using pip.
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed: {package}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}. Error: {e}")

# List of required libraries
required_libraries = [
    "google-generativeai",
    "pyttsx3",
    "SpeechRecognition",
    "pywhatkit",
    "opencv-python",
    "requests",
    "pyautogui",
    "pyaudio"  
]

# Install each library
for library in required_libraries:
    install(library)

print("All required libraries have been installed.")
