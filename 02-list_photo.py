import os
import csv

def list_files_to_csv(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_name = os.path.splitext(file)[0]
            file_path = os.path.join(root, file).replace("\\", "/")
            file_list.append({"KODE POHON": file_name, "PATH": file_path})

    csv_file = "file_list.csv"
    with open(csv_file, mode='w', newline='') as file:
        fieldnames = ["KODE POHON", "PATH"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(file_list)

    print(f"File list exported to {csv_file}")

# Usage example
directory = 'C:/Github/Belajar QGIS dan Alpine Quest/test_2024-02-18/photo_files'
list_files_to_csv(directory)