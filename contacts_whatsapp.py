import json

CONTACTS_FILE = 'contacts_whatsapp.json'

def load_contacts_whatsapp():
    """Load contacts from the JSON file."""
    try:
        with open(CONTACTS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file doesn't exist

def save_contacts_whatsapp(contact_dict):
    """Save contacts to the JSON file."""
    with open(CONTACTS_FILE, 'w') as file:
        json.dump(contact_dict, file, indent=4)
