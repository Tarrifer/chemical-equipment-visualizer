import requests

BASE_URL = "http://127.0.0.1:8001/api/equipment"
TOKEN_URL = "http://127.0.0.1:8001/api/token/"

_auth_token = None

def set_token(token):
    global _auth_token
    _auth_token = token

def _auth_headers():
    if not _auth_token:
        raise Exception("Not authenticated")
    return {"Authorization": f"Token {_auth_token}"}

def upload_csv(file_path):
    url = f"{BASE_URL}/upload/"

    with open(file_path, "rb") as f:
        response = requests.post(
            url,
            files={"file": f},
            headers=_auth_headers(),
        )

    response.raise_for_status()
    return response.json()

def download_pdf(save_path):
    url = f"{BASE_URL}/report/"

    response = requests.get(
        url,
        headers=_auth_headers(),
    )

    response.raise_for_status()

    with open(save_path, "wb") as f:
        f.write(response.content)

def get_auth_headers():
    return _auth_headers()