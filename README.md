# csvtokmz-ge-aqpro

## Purpose

Generate KMZ files from CSV data and images for use in Google Earth and Alpine Quest Pro.

## Features

- **Custom Icons**: Supports Google Earth icons via URLs defined in the CSV file.
- **Image Attachments**: Supports image attachments for each waypoint (via URL or local path).
- **Descriptions**: Supports descriptions for each waypoint.

## Installation

For Conda User

Create a conda environment using the provided environment.yml file:

```python
conda env create -f environment.yml
conda activate csvtokmz-ge-aqpro
```

For Pip User

Install the required packages using

```python
pip install -r requirements.txt
```

## Usage

1. **Prepare CSV File**: Ensure your CSV file is formatted correctly with columns for name, description, latitude, longitude, photo_path, and icon_url.
2. **Prepare Image Files**: If using local image paths, ensure the images are accessible at the specified paths.

### Using Jupyter Notebook or Python Script

```python
# Importing KMZ Generator from CSV
import sys
sys.path.append('path/to/your/project')  # Change to your project path
from src.kml_operations import generate_kmz_from_csv

csv_file = "path/to/your/csvfile.csv"  # Specify the location of your CSV file

# Run the generator
generate_kmz_from_csv(csv_file)

## Using Command Line Interface (CLI)

```python
python main.py generate --csv-file path/to/your/csvfile.csv --output-folder path/to/output/folder
```

## License

This project is licensed under the MIT License
