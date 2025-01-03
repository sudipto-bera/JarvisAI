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


# Configure Google Generative AI API
GENAI_API_KEY = api_data
genai.configure(api_key=GENAI_API_KEY)

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
engine.setProperty('voice', engine.getProperty('voices')[0].id)

def speak(text):
    """Speak the provided text using the TTS engine."""
    engine.say(text)
    engine.runAndWait()

def wish():
    """Greet the user based on the current time of day."""
    hour = int(dt.datetime.now().hour)

    if hour <= 0 and hour < 12:
        speak("Good morning")
    elif hour <= 12 and hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("I'm Jarvis, sir. Please tell me how can I help you?")

def listen_to_command():
    """Convert speech to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        conversation_area.insert(tk.END, "Listening...\n\n")
        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            query = recognizer.recognize_google(audio, language='en-in').lower()
            conversation_area.insert(tk.END, f"You: {query}\n")
            return query
        except sr.UnknownValueError:
            conversation_area.insert(tk.END, "Jarvis: Sorry, I didn't catch that. Please repeat.\n")
            speak("Sorry, I didn't catch that. Please repeat.")
            return "none"
        except sr.RequestError:
            conversation_area.insert(tk.END, "Jarvis: Network error. Please check your connection.\n")
            speak("Network error. Please check your connection.")
            return "none"
        except Exception as e:
            conversation_area.insert(tk.END, f"Jarvis: Error {e}\n")
            return "none"

def generate_response(query):
    """Generate a response for the given query using Gemini."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(query, generation_config=genai.GenerationConfig(
            max_output_tokens=75,
            temperature=0.1,
        ))
        return response.text
    except Exception as e:
        return f"Sorry, I encountered an error: {e}"

def news():
    try:
        # URL for fetching news with API key
        main_url = 'https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=8b344e617c7548ff9da0e6f2a7af1cf2'

        # Fetch news data as JSON
        main_page = requests.get(main_url).json()

        # Check if the API returned valid data
        if main_page.get("status") == "ok":
            articles = main_page.get("articles", [])

            # Check if there are any articles
            if len(articles) == 0:
                speak("I couldn't find any news at the moment.")
                return

            # Prepare the news headlines
            head = []
            day = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth']

            # Fetch the top news headlines
            for ar in articles:
                head.append(ar.get('title', 'No title available'))

            # Read out the top 10 news headlines
            for i in range(min(len(head), len(day))):  # Ensure we don't exceed available headlines
                speak(f"Today's {day[i]} news is: {head[i]}")
        else:
            speak("Unable to fetch news at the moment. Please try again later.")
    except Exception as e:
        # Handle errors gracefully
        speak("I encountered an issue while fetching the news.")
        print(f"Error: {e}")

def findContactAndSendMessage():
    try:
        # Load contacts dynamically
        contact_dict = load_contacts_whatsapp()

        speak("Who should I send the message to?")
        recipient_input = listen_to_command().lower()

        if recipient_input == "none":
            speak("I couldn't hear the contact name or phone number. Please try again.")
            return

        # Attempt to find the contact by name
        contact_details = contact_dict.get(recipient_input)

        # If not found by name, search by phone number
        if not contact_details:
            for contact in contact_dict.values():
                if contact.get("phone") == recipient_input:
                    contact_details = contact
                    break

        # If contact is still not found, raise an exception
        if not contact_details:
            raise ValueError("Contact not found by name or phone number.")

        # Extract contact details
        contact_name = contact_details["name"]

        # Open WhatsApp Web
        webbrowser.open("https://web.whatsapp.com/")
        speak("Opening WhatsApp Web. Please make sure you are logged in.")
        time.sleep(10)  # Wait for WhatsApp Web to load

        # Click on the search bar (coordinates may need adjustment)
        pyautogui.click(x=300, y=200)
        time.sleep(2)

        # Type the contact name
        pyautogui.typewrite(contact_name, interval=0.1)
        time.sleep(2)

        # Press Enter to open the chat
        pyautogui.press('enter')
        time.sleep(2)

        # Ask for the message to send
        speak("What message should I send?")
        message = listen_to_command()

        if message == "none":
            speak("I couldn't hear the message. Please try again.")
            return

        # Type the message in the chat box
        pyautogui.typewrite(message, interval=0.1)
        time.sleep(1)

        # Press Enter to send the message
        pyautogui.press('enter')
        speak("Message sent successfully!")

    except ValueError as ve:
        speak("I couldn't find the contact by name or phone number. Please try again.")
        print(f"Error: {ve}")
    except Exception as e:
        speak("An error occurred while finding the contact or sending the message.")
        print(f"Error: {e}")

def sendEmail(to, content):
    # Load email credentials
    credentials = load_credentials()
    your_email = credentials.get("your_email")
    your_password = credentials.get("your_password")

    if not your_email or not your_password:
        print("Error: Email credentials are not set.")
        return False

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Gmail SMTP server
        server.starttls()  # Secure the connection
        server.login(your_email, your_password)  # Login to your email account
        server.sendmail(your_email, to, content)  # Send the email
        server.close()  # Close the connection
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def handle_query(query):
    """Handle specific commands like opening or closing Notepad."""
    global cap

    if "open notepad" in query:
        speak("Opening Notepad...")
        try:
            subprocess.Popen(['notepad.exe'])  # Open Notepad
            conversation_area.insert(tk.END, "Jarvis: Notepad opened successfully.\n")
        except FileNotFoundError:
            speak("It seems Notepad is not available on this system.")
        except Exception as e:
            speak("I couldn't open Notepad due to an error.")
            print(f"An unexpected error occurred: {e}")
        return  # Prevent further processing

    elif "close notepad" in query:
        try:
            speak("Okay sir, closing Notepad.")
            os.system("taskkill /f /im notepad.exe")  # Forcefully closes Notepad
            speak("Notepad has been closed.")
            conversation_area.insert(tk.END, "Jarvis: Notepad has been closed.\n")
        except Exception as e:
            speak("I encountered an issue while trying to close Notepad.")
            print(f"Error: {e}")
        return  # Prevent further processing

    elif "play song on youtube" in query:
        try:
            speak("Which song should I play?")
            song_name = listen_to_command()  # Taking the song name as input via voice
            if song_name != "none":
                speak(f"Playing {song_name} on YouTube.")
                kit.playonyt(song_name)  # Using pywhatkit to play the song
                conversation_area.insert(tk.END, f"Jarvis: Playing {song_name} on YouTube.\n")
            else:
                speak("I couldn't hear the song name. Please try again.")
        except Exception as e:
            speak("An error occurred while trying to play the song.")
            print(f"Error: {e}")
        return  # Prevent further processing

    elif "open command prompt" in query:
        speak("Opening Command Prompt")
        try:
            os.startfile('cmd.exe')
            conversation_area.insert(tk.END, "Jarvis: Command Prompt opened successfully.\n")
        except FileNotFoundError:
            speak("It seems Command Prompt is not available on this system.")
        except Exception as e:
            speak("I couldn't open Command Prompt due to an error.")
            print(f"An unexpected error occurred: {e}")
        return  # Prevent further processing

    elif "close command prompt" in query:
        try:
            speak("Okay sir, closing Command Prompt.")
            os.system("taskkill /f /im cmd.exe")  # Forcefully closes all Command Prompt instances
            speak("Command Prompt has been closed.")
            conversation_area.insert(tk.END, "Jarvis: Command Prompt has been closed.\n")
        except Exception as e:
            speak("I encountered an issue while trying to close Command Prompt.")
            print(f"Error: {e}")
        return  # Prevent further processing

    elif "open camera" in query:
        speak("Opening the camera...")

        try:
            cap = cv2.VideoCapture(0)  # Open the default webcam
            if not cap.isOpened():
                speak(
                    "I couldn't access the webcam. Please check if it's connected or in use by another application.")
            else:
                camera_active = True
                while camera_active:
                    ret, img = cap.read()
                    if not ret:
                        speak("I couldn't capture the video feed. Please check the webcam.")
                        break
                    cv2.imshow('Webcam', img)
                    # Check for 'ESC' key to close manually
                    if cv2.waitKey(1) & 0xFF == 27:
                        break

                    # Check if the user says "close camera"

                    query = listen_to_command().lower()  # Listen for a new command

                    if 'close camera' in query:
                        speak("Closing the camera.")
                        camera_active = False
                cap.release()
                cv2.destroyAllWindows()
                speak("Camera closed.")

        except Exception as e:
            speak("An error occurred while trying to access the camera.")
            print(f"Error: {e}")
        return  # Prevent further processing

    elif "close camera" in query:
        try:
            if 'cap' in globals() and cap.isOpened():
                cap.release()
            cv2.destroyAllWindows()
            speak("Camera has been closed.")
            conversation_area.insert(tk.END, "Jarvis: Camera has been closed.\n")
        except Exception as e:
            speak("I encountered an issue while trying to close the camera.")
            print(f"Error: {e}")
        return  # Prevent further processing

    elif "ip address" in query:
        try:
            ip = get('https://api.ipify.org').text
            speak(f"Your IP address is {ip}")
            conversation_area.insert(tk.END, f"Jarvis: Your IP address is {ip}.\n")
        except Exception as e:
            speak("Sorry, I couldn't fetch the IP address. Please check your internet connection.")
            print(f"Error: {e}")
        return  # Prevent further processing


    elif "switch window" in query:
        try:
            speak("Switching the window, sir.")
            pyautogui.keyDown('alt')  # Hold the 'Alt' key
            pyautogui.press('tab')  # Press the 'Tab' key to switch windows
            time.sleep(2)  # Add a short delay to ensure the command is executed
            pyautogui.keyUp('alt')  # Release the 'Alt' key
            speak("Window switched.")
        except Exception as e:
            speak("I encountered an issue while trying to switch the window.")
            print(f"Error: {e}")
        return  # Prevent further processing

    elif "tell me news" in query:
        speak("Please wait, sir. Fetching the latest news.")
        news()
        return  # Prevent further processing

    # to send message in whatsapp
    elif 'send message' in query:
        findContactAndSendMessage()
        return # Prevent further processing

    elif "email to" in query or "send email" in query:
        try:
            speak('Who should I send the email to?')
            recipient_name = listen_to_command().lower()

            # Load contacts dynamically
            email_dict = load_contacts()

            if recipient_name in email_dict:
                to = email_dict[recipient_name]
                speak('What should I say?')
                content = listen_to_command().lower()
                if sendEmail(to, content):
                    speak('Email has been sent successfully.')
                else:
                    speak('I was unable to send the email. Please check the details.')
            else:
                speak("I don't have an email address for this contact.")
        except Exception as e:
            print(e)
            speak("Sorry, I'm unable to send the email right now.")

        return

    # Pass the query to the Gemini API if no specific commands are handled
    response = generate_response(query)
    conversation_area.insert(tk.END, f"Jarvis: {response}\n")
    speak(response)

stop_conversation = False

def handle_conversation():
    """Continuously listen to user input and respond."""
    global stop_conversation
    while not stop_conversation:
        query = listen_to_command()
        if query == "none":
            continue
        if "bye" in query or "goodbye" in query or "exit" in query or "stop" in query:
            conversation_area.insert(tk.END, "Jarvis: Goodbye! Have a great day!\n")
            speak("Goodbye! Have a great day!")
            break
        handle_query(query)

def start_conversation():
    """Start the conversation with a greeting and initialize the conversation thread."""
    global stop_conversation
    stop_conversation = False
    conversation_thread = threading.Thread(target=handle_conversation)
    conversation_thread.daemon = True
    conversation_thread.start()
    conversation_area.insert(tk.END, "Hi, I am Jarvis. How can I help you?\n\n")
    conversation_area.see(tk.END)
    wish()

def end_conversation():
    """End the conversation and close the application."""
    global stop_conversation
    stop_conversation = True
    conversation_area.insert(tk.END, "Jarvis: Conversation ended manually. Goodbye!\n")
    speak("Conversation ended manually. Goodbye!")
    root.quit()

# Set up the GUI
root = tk.Tk()
root.title("J-A-R-V-I-S")

# Conversation display area
conversation_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, font=("Arial", 12))
conversation_area.pack(padx=10, pady=10)

# Start conversation button
start_button = tk.Button(root, text="Start Conversation", font=("Arial", 12), command=start_conversation)
start_button.pack(pady=5)

# End conversation button
end_button = tk.Button(root, text="End Conversation", font=("Arial", 12), command=end_conversation)
end_button.pack(pady=5)

# Run the GUI event loop
root.mainloop()
