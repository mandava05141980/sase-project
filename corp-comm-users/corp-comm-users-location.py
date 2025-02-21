import csv
import requests

API_TOKEN = "23bf69f3c8f559"  # Replace with your actual API token
BASE_API_URL = "https://ipinfo.io/"

def get_ip_location(ip_address):
    try:
        api_url = f"{BASE_API_URL}{ip_address}/json?token={API_TOKEN}"
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for 4XX and 5XX status codes
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error fetching location for IP {ip_address}: {e}")
        return {}

# Read CSV file, update data, and write back to the same file
csv_file_path = r"C:\Lakshmi\Autodesk\KT\Python\Autodesk-Projects\sase-project\corp-comm-users\report.csv"

with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    fieldnames = reader.fieldnames + ['City', 'Region', 'Country']
    
    # Create a temporary list to store the updated rows
    updated_rows = []
    
    for row in reader:
        ip_address = row['IP']  # Assuming 'IP' is the column containing IP addresses
        location_info = get_ip_location(ip_address)
        
        # Update the row with location information
        row['City'] = location_info.get('city', '')
        row['Region'] = location_info.get('region', '')
        row['Country'] = location_info.get('country', '')
        
        updated_rows.append(row)

# Write the updated data back to the CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write the header
    writer.writeheader()
    
    # Write the updated rows
    writer.writerows(updated_rows)
