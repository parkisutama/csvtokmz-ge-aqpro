from src.kml_operations import create_kml
from src.kml_operations import create_kmz
from src.data_processing import process_photos_and_icons
from src.config import OUTPUT_FOLDER
import pandas as pd
import os
from datetime import datetime


def generate_kmz_from_csv(csv_file: str, output_folder: str = OUTPUT_FOLDER) -> str:
    """
    Main function to generate a KMZ file from a CSV file.

    Args:
        csv_file (str): Path to the input CSV file.
        output_folder (str): Directory to save the generated KMZ file.

    Returns:
        str: Path to the generated KMZ file.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Read and process the CSV
    dataframe = pd.read_csv(csv_file)
    dataframe = process_photos_and_icons(dataframe)

    # Create KML
    kml_file = os.path.join(output_folder, "doc.kml")
    folder_name = os.path.splitext(os.path.basename(csv_file))[0]
    create_kml(dataframe, kml_file, folder_name)

    # Create KMZ
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = os.path.join(output_folder, f"output_{timestamp}.kmz")
    create_kmz(kml_file, dataframe, output_file)

    return output_file
