import json

# File to store the credentials
CREDENTIALS_FILE = 'credentials.json'

def load_credentials():
    """Load email credentials from the JSON file."""
    try:
        with open(CREDENTIALS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"your_email": "", "your_password": ""}  # Return empty fields if file doesn't exist

def save_credentials(email, password):
    """Save email credentials to the JSON file."""
    credentials = {
        "your_email": email,
        "your_password": password
    }
    with open(CREDENTIALS_FILE, 'w') as file:
        json.dump(credentials, file, indent=4)
