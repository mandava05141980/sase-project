import pandas as pd
from sasepolicy import get_token, create_address, create_address_group, create_security_rule

# Replace 'your_file.xlsx' with the actual file path or URL
file_path = '/Lakshmi/Autodesk/KT/Python/Autodesk-Projects/sase-project/On-Prem-VPN/On-Prem-Dev/dc_accounts1.xlsx'

# Read only the 'app' column and other required columns from the Excel file
df = pd.read_excel(file_path, usecols=['app', 'ip', 'group', 'serviceid', 'secgroup'])

# Group by 'app' and aggregate 'ip', 'group', 'serviceid', and 'secgroup' columns as lists
grouped = df.groupby('app').agg({
    'ip': list,
    'group': list,
    'serviceid': list,
    'secgroup': list
}).reset_index()

# Define the functions here
def create_address_wrapper(app, ip_addresses, cidr_list):
    for ip_address, cidr in zip(ip_addresses, cidr_list):
        print("Calling Create Address API for account", app)
        create_address(app, ip_address, cidr)

def create_address_group_wrapper(app, cidr_list):
    print("Calling Create Address Group API for account", app)
    create_address_group(app, cidr_list)

def create_security_rule_wrapper(app, secgroups, serviceid):
    print("Calling Security Rule API for account", app)
    create_security_rule(app, secgroups, serviceid)

# Iterate over grouped data and prepare records for API calls
for index, row in grouped.iterrows():
    app = row['app']
    print("App: ", app)

    # Replace '.' and '/' in IP addresses with '_' and append "_Vpn"
    cidr_list = [str(ip).replace('.', '_').replace('/','_') + "_CIDR" for ip in row['ip'] if pd.notna(ip)]


    # Call the create_address function
    create_address_wrapper(app, row['ip'], cidr_list)

    # Call the create_address_group function
    create_address_group_wrapper(app, cidr_list)

    # Call the create_security_rule function
    create_security_rule_wrapper(app, row['secgroup'], row['serviceid'])

    print("***********************************************************")
