import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Automatically install required libraries
install("google-generativeai")
install("pyttsx3")
install("SpeechRecognition")
install("pywhatkit")
install("opencv-python")
install("requests")
install("pyautogui")

# Import Libraries
def main():
    import google.generativeai as genai
    import pyttsx3
    import speech_recognition as sr
    import tkinter as tk
    from tkinter import scrolledtext
    import threading
    from apikey import api_data
    import datetime as dt
    import subprocess
    import os
    import pywhatkit as kit
    import cv2
    import requests
    from requests import get
    import pyautogui
    import time
    import webbrowser
    import smtplib
    from contacts import load_contacts
    from contacts_whatsapp import load_contacts_whatsapp
    from credentials import load_credentials

    # Add your main logic here
    print("All libraries are installed and imported successfully.")

if __name__ == "__main__":
    main()
