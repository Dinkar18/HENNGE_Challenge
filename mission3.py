import requests
import hmac
import hashlib
import time
import struct
import json
from requests.auth import HTTPBasicAuth

# Replace with your email
USERID = "aryadinkar027@gmail.com"

# API Endpoint
ROOT = "https://api.challenge.hennge.com/challenges/003"

# Constants for TOTP
SECRET_SUFFIX = "HENNGECHALLENGE003"
SHARED_SECRET = USERID + SECRET_SUFFIX
TIMESTEP = 30
T0 = 0
DIGITS = 10

# Replace with your actual GitHub Gist URL
GITHUB_GIST_URL = "https://gist.github.com/YOUR_ACCOUNT/GIST_ID"

# Data payload for submission
data = {
    "github_url": GITHUB_GIST_URL,
    "contact_email": USERID,
    "solution_language": "python"  # Change to "golang" if using Go
}

def HOTP(K, C, digits=10):
    """HOTP: Generates an HMAC-based OTP"""
    K_bytes = K.encode()
    C_bytes = struct.pack(">Q", C)
    hmac_sha512 = hmac.new(K_bytes, C_bytes, hashlib.sha512).hexdigest()
    return Truncate(hmac_sha512)[-digits:]

def Truncate(hmac_sha512):
    """Truncates HMAC-SHA-512 output to extract OTP"""
    offset = int(hmac_sha512[-1], 16)
    binary = int(hmac_sha512[(offset * 2):((offset * 2) + 8)], 16) & 0x7FFFFFFF
    return str(binary)

def TOTP(K, digits=10, timeref=0, timestep=30):
    """TOTP: Time-based OTP variant of HOTP"""
    C = int(time.time() - timeref) // timestep
    return HOTP(K, C, digits=digits)

# Generate 10-digit TOTP password
passwd = TOTP(SHARED_SECRET, DIGITS, T0, TIMESTEP).zfill(10)

# Encode authorization credentials
auth_header = HTTPBasicAuth(USERID, passwd)

# Send request
headers = {"Content-Type": "application/json"}
response = requests.post(ROOT, auth=auth_header, headers=headers, data=json.dumps(data))

# Print server response
print(response.status_code, response.text)
