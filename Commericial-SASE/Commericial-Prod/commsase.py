from ast import parse
from tokenize import Token
import requests
import json
import pandas as pd
import numpy as np
from numpy import nan


def get_token():
    token_url = "https://auth.apps.paloaltonetworks.com/auth/v1/oauth2/access_token?grant_type=client_credentials&scope=tsg_id:1875144976"
    username = "sasemonitoring@1875144976.iam.panserviceaccount.com"
    password = "ce5478df-25be-4172-9c4c-6d40d0088fe6"

    
    headers = {
        'Content-Type': 'application/json'
        }
    payload = {}

    #API call to create address
    response = requests.request("POST",token_url, headers=headers, auth=(username, password), data=payload)
    #print("Get Token response code", response.status_code)
    data = response.text
    parse_json = json.loads(data)
    Token = parse_json["access_token"]
    return Token

def create_address(app, ip, cidr_list):
    create_address_url = "https://api.sase.paloaltonetworks.com/sse/config/v1/addresses?folder=Mobile Users Container"
    Token = get_token()
    payload = json.dumps({
        "description": "Address for " + str(app),
        "name": cidr_list,
        "ip_netmask": ip
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + Token
    }
    try:
        response = requests.post(create_address_url, headers=headers, data=payload)
        print(response.text)
        if response.status_code == 201:
            print("Create address API successful for account", str(app))
        else:
            print("Create address API NOT successful for account", str(app))
    except Exception as e:
        print(e)

def create_address_group(app, cidr_list):
    create_address_url = "https://api.sase.paloaltonetworks.com/sse/config/v1/address-groups?folder=Mobile Users Container"
    Token = get_token()
    payload = json.dumps({
        "description": "Address group for " + str(app),
        "name": str(app) + "-CIDR",
        "static": cidr_list
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + Token
    }
    try:
        response = requests.post(create_address_url, headers=headers, data=payload)
        print(response.text)
        if response.status_code == 201:
            print("Create address Group API successful for account", str(app))
        else:
            print("Create address Group API NOT successful for account", str(app))
    except Exception as e:
        print(e)

def create_security_rule(app, secgroup):
    print("secgroup from Excel:", secgroup)  # Debugging print

    # Filter out NaN values from secgroup
    secgroup = [group for group in secgroup if pd.notna(group)]
    print("Filtered secgroup:", secgroup)  # Debugging print
    
    # Check if secgroup is empty
    if not secgroup:
        print("No valid source groups found for", app)
        return
    
    description = f"Allows all network traffic for authorized users to all: {app}"
    tag_name = f"VPN-Policy-Commercial-{app}"

    create_address_url = "https://api.sase.paloaltonetworks.com/sse/config/v1/security-rules?position=post&folder=Mobile Users Container"
    Token = get_token()  # Assuming get_token function is defined elsewhere
    
    # Format secgroup data for source_user field
    source_users = [f"CN={group},DC=adskeng,DC=net" for group in secgroup]

    # Modify the payload to include secgroup data
    payload = {
        "action": "allow",
        "application": ["any"],
        "category": ["any"],
        "description": description,
        "destination": [f"{app}-CIDR"],
        "destination_hip": ["any"],
        "disabled": True,
        "from": ["trust"],
        "log_setting": "Cortex Data Lake",
        "name": f"ALLOW_ALL_TRAFFIC_TO_ALL_IN_{app}",
        "negate_destination": False,
        "negate_source": False,
        "profile_setting": {"group": ["ADSK-security-profile-group"]},
        "service": ["any"],
        "source": ["ADSK-POOL"],
        "source_hip": ["ADSK-HIP-Workstation-Profile"],
        "source_user": source_users,  # Use formatted secgroup data here
        "tag": [tag_name], 
        "to": ["trust"]
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {Token}'
    }

    try:
        response = requests.post(create_address_url, headers=headers, json=payload)
        print(response.text)
        if response.status_code == 201:
            print("Create Security Rule API successful for account", app)
        else:
            print("Create Security Rule API NOT successful for account", app)
    except Exception as e:
        print(e)





