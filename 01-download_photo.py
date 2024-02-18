import os
import pandas as pd
import requests

# Function to download image from URL
def download_image(url, folder, filename, log):
    filepath = os.path.join(folder, filename)
    if os.path.exists(filepath):
        log.write(f"Duplicate: {filename} already exists\n")
        print(f"Duplicate: {filename} already exists")
        return False  # File already exists, skip download
    else:
        log.write(f"Downloading: {filename}\n")
        print(f"Downloading: {filename}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filepath, 'wb') as file:
                file.write(response.content)
            log.write(f"Downloaded: {filename}\n")
            print(f"Downloaded: {filename}")
            return True
        else:
            log.write(f"Failed to download: {filename}\n")
            print(f"Failed to download: {filename}")
    except requests.exceptions.RequestException as e:
        log.write(f"Failed to download: {filename} - {str(e)}\n")
        print(f"Failed to download: {filename} - {str(e)}")
    return False

# Function to print the content of the CSV file
def print_csv_content(csv_path):
    df = pd.read_csv(csv_path, delimiter=';')
    print(df)

# Function to download data from CSV
def download_data(csv_path, download_folder, log_file):
    # Print CSV content
    print_csv_content(csv_path)

    # Read CSV file
    df = pd.read_csv(csv_path, delimiter=',')

    # Create folder if not exists
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Open log file for writing
    with open(log_file, 'w') as log:
        # Iterate through each row in the CSV
        for index, row in df.iterrows():
            # Get tree code and photo URL
            tree_code = str(row['KODE POHON'])
            photo_url = str(row['FOTO POHON P1'])

            # Download and save image
            success = download_image(photo_url, download_folder, f"{tree_code}.jpg", log)

# Specify the path to your CSV file, the folder to save photos, and the log file
csv_path = 'C:/Github/Belajar QGIS dan Alpine Quest/test_2024-02-18/source_2.csv'  # Update this path
download_folder = 'C:/Github/Belajar QGIS dan Alpine Quest/test_2024-02-18/photo_files'  # Update this path
log_file = 'C:/Github/Belajar QGIS dan Alpine Quest/test_2024-02-18/log_file.txt'  # Update this path

# Download data
download_data(csv_path, download_folder, log_file)
 