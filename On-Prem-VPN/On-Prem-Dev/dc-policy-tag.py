import pandas as pd
import requests

# Function to get the access token
def get_token():
    token_url = "https://auth.apps.paloaltonetworks.com/auth/v1/oauth2/access_token?grant_type=client_credentials&scope=tsg_id:1231960117"
    username = "sasemonitoring@1231960117.iam.panserviceaccount.com"
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
def create_tag(app, serviceid, token):
    url = "https://api.sase.paloaltonetworks.com/sse/config/v1/tags?folder=Mobile Users Container"
    payload = {
        "color": "Red",
        "comments": f"VPN-Policy-DC-{app}-{serviceid}",
        "name": f"VPN-Policy-DC-{app}-{serviceid}"
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f"Tag created successfully for {app}-{serviceid}")
    else:
        print(f"Failed to create tag for {app}-{serviceid}: {response.text}")

# Read the Excel file and extract 'app' and 'serviceid' columns
file_path = '/Lakshmi/Autodesk/KT/Python/Autodesk-Projects/sase-project/On-Prem-VPN/On-Prem-Dev/dc_accounts1.xlsx'
df = pd.read_excel(file_path, usecols=['app', 'serviceid'])

# Retrieve the token
token = get_token()
if token:
    for index, row in df.iterrows():
        app = row['app']
        serviceid = row['serviceid']
        # Check if serviceid is not null or NaN
        if pd.notna(serviceid):
            create_tag(app, serviceid, token)
        else:
            print(f"Skipping tag creation for {app} as serviceid is null or NaN")
