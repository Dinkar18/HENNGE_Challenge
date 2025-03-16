import hmac
import hashlib
import struct
import time
import base64
import requests
import json

# Configuration
EMAIL = "aryadinkar027@gmail.com"  
GIST_URL = "https://gist.github.com/Dinkar18/d01a634e74ca35a5d015c5fb7f693327#file-mission3-py"  
SECRET_KEY = EMAIL + "HENNGECHALLENGE003"
API_URL = "https://api.challenge.hennge.com/challenges/003"

def generate_totp(secret, time_step=30, digits=10):
    """Generate a 10-digit TOTP using HMAC-SHA-512."""
    counter = int(time.time() // time_step)
    msg = struct.pack(">Q", counter)
    hmac_digest = hmac.new(secret.encode(), msg, hashlib.sha512).digest()
    offset = hmac_digest[-1] & 0x0F
    binary_code = struct.unpack(">I", hmac_digest[offset:offset + 4])[0] & 0x7FFFFFFF
    return str(binary_code)[-digits:]

def send_request():
    """Prepare JSON payload, generate TOTP, and send the API request."""
    totp_password = generate_totp(SECRET_KEY)
    auth_header = base64.b64encode(f"{EMAIL}:{totp_password}".encode()).decode()

    payload = {
        "github_url": GIST_URL,
        "contact_email": EMAIL,
        "solution_language": "python"
    }

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/json",
        "Accept": "*/*"
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    print("Status Code:", response.status_code)
    print("Response:", response.text)

if __name__ == "__main__":
    send_request()
