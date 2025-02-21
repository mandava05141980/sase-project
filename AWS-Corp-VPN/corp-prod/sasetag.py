from ast import parse
from tokenize import Token
import requests
import json
import pandas as pd
import numpy as np
from numpy import nan


def get_token():
    token_url = "https://auth.apps.paloaltonetworks.com/auth/v1/oauth2/access_token?grant_type=client_credentials&scope=tsg_id:1047793671"
    username = "sasemonitoring@1047793671.iam.panserviceaccount.com"
    password = "07a31634-9b77-48c5-a107-cd0f78d45889"

    
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

def create_security_rule(app, vpc, serviceid, env):
    # Filter out NaN values from secgroup and serviceid
    #secgroup = [group for group in secgroup if pd.notna(group)]
    serviceid = [str(id) for id in serviceid if pd.notna(id)]
    # Convert app to a string and pad with leading zeros to ensure it has a specific width
    app_str = str(app).zfill(12)  # Assuming you want the width to be 12 characters

    # Check if secgroup and serviceid are not empty
    #if not secgroup:
     #   print("No valid source groups found for", app)
       # return
    if not serviceid:
        print("No valid service IDs found for", app)
        return 
    if isinstance(env, list):
        env_str = ', '.join(str(item) for item in env if pd.notna(item))
    else:
        env_str = str(env)
    if isinstance(vpc, list):
        vpc_str = ', '.join(str(item) for item in vpc if pd.notna(item))
    else:
        vpc_str = str(vpc)

    description = f"Allows all network traffic for authorized users to all: {app}-{env_str}"

    # Construct the tag name, handling NaN values and invalid characters
    tag_name = f"VPN-Policy-AWS-Corp-{vpc_str}-{'-'.join(serviceid)}"

    create_address_url = "https://api.sase.paloaltonetworks.com/sse/config/v1/security-rules?position=post&folder=Mobile Users Container"
    Token = get_token()
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
        "source_user": [
    r"CN=SG-AWS-" + app_str + "-Deployer,DC=autodesk,DC=com",
    r"CN=SG-AWS-" + app_str + "-Owner,DC=autodesk,DC=com",
    r"CN=SG-AWS-" + app_str + "-Viewer,DC=autodesk,DC=com"         
],
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
