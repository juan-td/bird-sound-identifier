# Download from xeno-canto.org using the xeno-canto API
# Usage: python download_script.py <output_dir> <query>

import requests
import sys
import time
import os

def download_recordings(output_dir, query):
    base_url = "https://xeno-canto.org/api/2/recordings"
    page = 1

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    csv_file_path = os.path.join(output_dir, 'recordings.csv')

    if not os.path.exists(csv_file_path):        
        with open(csv_file_path, 'w') as csv_file:
            csv_file.write('file_name,en_species\n')
    
    while True:
        response = requests.get(f"{base_url}?query={query}&page={page}")
        data = response.json()

        if 'recordings' not in data or not data['recordings']:
            break

        for recording in data['recordings']:
            file_url = recording['sono']['med']
            file_name = os.path.join(output_dir, file_url.split('/')[-1].split('-')[0] + '.png')
            file_response = requests.get('https:'+file_url)

            with open(file_name, 'wb') as f:
                f.write(file_response.content)
            
            with open(csv_file_path, 'a') as csv_file:
                csv_file.write(f"{file_name.split('/')[-1]},{recording['en']}\n")
                


        page += 1
        time.sleep(2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python download_script.py <output_dir> <query>")
        sys.exit(1)

    output_dir = sys.argv[1]
    query = sys.argv[2]
    download_recordings(output_dir, query)