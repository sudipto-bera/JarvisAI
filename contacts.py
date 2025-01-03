import json

# File to store the contacts
CONTACTS_FILE = 'contacts.json'

def load_contacts():
    """Load contacts from the JSON file."""
    try:
        with open(CONTACTS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file doesn't exist

def save_contacts(contacts):
    """Save contacts to the JSON file."""
    with open(CONTACTS_FILE, 'w') as file:
        json.dump(contacts, file, indent=4)
