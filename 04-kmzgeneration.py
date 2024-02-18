import pandas as pd
import simplekml
from datetime import datetime
import zipfile
import os

# Modify the DataFrame loading to check and download images if needed
csv_file = 'C:/Github/Belajar QGIS dan Alpine Quest/test_2024-02-18/sourcemap.csv'
dataframe = pd.read_csv(csv_file)

# Create a new KML object using simplekml library
kml = simplekml.Kml()

# Get the name of the CSV file without the extension, and use it to name the waypoints folder
waypoints_foldername = os.path.splitext(os.path.basename(csv_file))[0]

# Create a folder to hold the waypoints with the name of the CSV file
folder = kml.newfolder(name=waypoints_foldername)

for index, row in dataframe.iterrows():
    # Generate the name using 'SUB BLOK' and 'KODE POHON'
    name_combined = f"{row['SUB BLOK P2']}-{row['KODE POHON']}"
    
    # Create a point for this row using the combined name
    point = folder.newpoint(name=name_combined, description=row['JENIS POHON P1'])
    
    # Set the coordinates for this point
    point.coords = [(row['LNG P1'], row['LAT P1'])]
    
    # If there is a photo path for this row, add it to the point's description
    if 'PATH' in row and pd.notnull(row['PATH']):
        photo_filename = os.path.basename(row['PATH'])
        photo_src = f"<img width='480' src='files/{photo_filename}'><br />"  # Modify the image source path so kmz photos will be inside "/files" in kmz
        point.description = f"{row['JENIS POHON P1']}<br /><br />{photo_src}" # will work as description
        
        # Add extended data for the photo path
        point.extendeddata.newdata(name='wptPhotos', value=f'files/{photo_filename}')

# Save the KML to a temporary file
kml_file = 'doc.kml'
kml.save(kml_file)

# Define the output file name
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
output_file = f'output_{timestamp}.kmz'

# Create a new ZIP file and add the KML file to it
with zipfile.ZipFile(output_file, 'w') as myzip:
    myzip.write(kml_file)
    # Add each photo to the ZIP file
    for PATH in dataframe['PATH'].unique():
        if pd.notnull(PATH) and os.path.isfile(PATH):
            myzip.write(PATH, arcname=f"files/{os.path.basename(PATH)}")  # Include "files" directory in arcname

# Delete the temporary KML file
os.remove(kml_file)

print(f"KMZ file saved: {output_file}")
