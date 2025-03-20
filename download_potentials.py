from lxml import html
import os
import requests

# Splits a file path into its components recursively
def split_path(path):
    head, tail = os.path.split(path)
    return split_path(head) + [tail] if head else [tail]

# Recursively enters subdirectories and downloads the file if it does not exist
def enter_subfolder(path_parts, pot_path):
    if len(path_parts) == 1:
        # Final subfolder, check if the file exists before downloading
        if not os.path.exists(path_parts[0]):
            os.system(f'wget {pot_path}')
        else:
            print(f'<{pot_path}> exists, skipping download')
    else:
        folder = path_parts.pop(0)
        os.makedirs(folder, exist_ok=True)  # Create folder if it doesn't exist
        os.chdir(folder)
        enter_subfolder(path_parts, pot_path)

# Base URL for downloading potentials
NIST_ROOT = 'https://www.ctcms.nist.gov/potentials/Download'
DOWNLOAD_FILE = 'Download'

# Download the main page containing potential file links
response = requests.get(NIST_ROOT)
if response.status_code != 200:
    print("Failed to download the main page")
    exit(1)

# Parse the HTML content
htmldoc = html.fromstring(response.content)
pots = htmldoc.find_class('panel-body')[0][0]

# Get current working directory
CWD = os.getcwd()

# Process each potential file link
for pot in pots:
    pot = str(html.tostring(pot[0])).split('"')[1][2:]
    if 'orkshop' not in pot:  # Filter out unwanted links
        path_parts = split_path(pot)
        os.chdir(CWD)
        enter_subfolder(path_parts, f'{NIST_ROOT}/{pot}')

# Return to the original directory
os.chdir(CWD)

# Create a timestamp file to mark the last download
timestamp_file = '_last_download.timestamp'
with open(timestamp_file, 'w') as f:
    f.write('Download completed.')

print(f"Download process completed. Timestamp file '{timestamp_file}' created.")