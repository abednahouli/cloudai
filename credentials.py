import json
import os

CREDENTIALS_FILE = "credentials.json"

def store_credentials(do_token, ssh_fingerprint):
    creds = {"do_token": do_token, "ssh_fingerprint": ssh_fingerprint}
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(creds, f)
    return True

def get_credentials():
    if not os.path.exists(CREDENTIALS_FILE):
        return None
    with open(CREDENTIALS_FILE, "r") as f:
        return json.load(f)
