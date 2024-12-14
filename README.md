# csvtokmz-ge-aqpro

## Purposegenerate_kmz_from_csv(csv)

Generate KMZ from CSV and Images for Google Earth and Alpine Quest Pro

## Features

- Custom Icon: Supported Google Earth Icon via URL defined in CSV File
- Image Attachment: Supported Image Attachment in each waypoint (via URL or Local Path)
- Description: Supported Description in each waypoint

## Usage

1. Prepare CSV File
2. Prepare Image Files (Optional only if image local path is defined in CSV)
3. use Jupyter Notebook or Python Script to run the generator

```python
# Importing KMZ Generator from CSV
import sys
sys.path.append('d:/project/csvtokmz-ge-aqpro/') # Change to your path
from src.kml_operations import generate_kmz_from_csv
csv = "D:/project/csvtokmz-ge-aqpro/data/processed/lokas_peta.csv" # Specify CSV Location File
```

4. Run the Generator

```python
generate_kmz_from_csv(csv)
```
