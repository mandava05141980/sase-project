import pandas as pd
import requests

# Function to get the access token
def get_token():
    token_url = "https://auth.apps.paloaltonetworks.com/auth/v1/oauth2/access_token?grant_type=client_credentials&scope=tsg_id:1498252864"
    username = "sasefedrampmonitoring@1498252864.iam.panserviceaccount.com"
    password = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    headers = {'Content-Type': 'application/json'}
    payload = {}

    response = requests.post(token_url, headers=headers, auth=(username, password), data=payload)
    if response.status_code == 200:
        parse_json = response.json()
        return parse_json.get("access_token")
    else:
        print("Failed to obtain token:", response.text)
        return None

# Function to create tags
def create_tag(app, token):
    url = "https://api.sase.paloaltonetworks.com/sse/config/v1/tags?folder=Mobile Users"
    payload = {
        "color": "Red",
        "comments": f"VPN-Policy-FedRAMP-{app}",
        "name": f"VPN-Policy-FedRAMP-{app}"
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f"Tag created successfully for {app}")
    elif response.status_code == 400 and "OBJECT_ALREADY_EXISTS" in response.text:
        print(f"Tag already exists for {app}")
    else:
        print(f"Failed to create tag for {app}: {response.text}")

# Read the Excel file and extract 'app' column
file_path = '/Users/mandavl1/Desktop/Autodesk-Bkp-09032024/Autodesk/KT/Python/Autodesk-Projects/sase-project/FedRAMP-VPN/fedramp.xlsx'

df = pd.read_excel(file_path, usecols=['app'])

# Retrieve the token
token = get_token()
if token:
    for index, row in df.iterrows():
        app = row['app']
        
        # Check if serviceid is not null or NaN
        if pd.notna(app):
            create_tag(app, token)
        else:
            print(f"Skipping tag creation for {app} as serviceid is null or NaN")