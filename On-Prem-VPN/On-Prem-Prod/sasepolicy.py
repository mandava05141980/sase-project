from ast import parse
from tokenize import Token
import requests
import json
import pandas as pd


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

def create_security_rule(app, secgroup, serviceid):
    # Filter out NaN values from secgroup
    secgroup = [group for group in secgroup if pd.notna(group)]

    create_address_url = "https://api.sase.paloaltonetworks.com/sse/config/v1/security-rules?position=post&folder=Mobile Users Container"
    Token = get_token()
    payload = json.dumps({
        "action": "allow",
        "application": ["any"],
        "category": ["any"],
        "description": "Allows all network traffic for authorized users to all: " + str(app),
        "destination": [str(app) + "-CIDR"],
        "destination_hip": ["any"],
        "disabled": True,
        "from": ["trust"],
        "log_setting": "Cortex Data Lake",
        "name": "ALLOW_ALL_TRAFFIC_TO_ALL_IN_" + str(app),
        "negate_destination": False,
        "negate_source": False,
        "profile_setting": {"group": ["ADSK-security-profile-group"]},
        "service": ["any"],
        "source": ["ADSK-POOL"],
        "source_hip": ["ADSK-HIP-Workstation-Profile"],
        #"source_user": [str(secgroup)],
        "source_user": secgroup,
        "tag": ["VPN-Policy-DC-" + str(app) + "-" + str(id) for id in serviceid if pd.notna(id)],
        #"tag": ["VPN-policy-active_directory-0AA80221"],
        "to": ["trust"]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + Token
    }
    try:
        response = requests.post(create_address_url, headers=headers, data=payload)
        print(response.text)
        if response.status_code == 201:
            print("Create Security Rule API successful for account", str(app))
        else:
            print("Create Security Rule API NOT successful for account", str(app))
    except Exception as e:
        print(e)
