import os
from datetime import datetime
import zipfile
import simplekml
import pandas as pd
from src.data_processing import process_media_files
from src.config import PHOTO_FOLDER, ICON_FOLDER, OUTPUT_FOLDER
import logging

# Ensure the OUTPUT_FOLDER directory exists
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Configure logging to write to a file inside OUTPUT_FOLDER
log_file_path = os.path.join(OUTPUT_FOLDER, "status.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file_path), logging.StreamHandler()],
)


def create_kml(df: pd.DataFrame, output_kml: str, folder_name: str):
    """
    Create a KML file from the dataframe.
    """
    kml = simplekml.Kml()
    folder = kml.newfolder(name=folder_name)

    for _, row in df.iterrows():
        point = folder.newpoint(
            name=row.get("name", ""), description=row.get("description", "")
        )
        point.coords = [(row["longitude"], row["latitude"])]

        # Attach photo
        if pd.notnull(row.get("photo_path")):
            photo_filename = os.path.basename(row["photo_path"])
            point.description += (
                f"<br /><img width='480' src='files/{photo_filename}'><br />"
            )
            point.extendeddata.newdata(
                name="wptPhotos", value=f"files/{photo_filename}"
            )

        # Attach custom icon
        if pd.notnull(row.get("icon_url")):
            icon_filename = os.path.basename(row["icon_url"])
            point.style.iconstyle.icon.href = f"files/{icon_filename}"

    kml.save(output_kml)


def create_kmz(kml_file: str, df: pd.DataFrame, output_file: str):
    """
    Create a KMZ file containing the KML and associated files.
    """
    with zipfile.ZipFile(output_file, "w") as zipf:
        zipf.write(kml_file, arcname="doc.kml")
        for column in ["photo_path", "icon_url"]:
            for file_path in df[column].dropna().unique():
                if os.path.exists(file_path):
                    zipf.write(
                        file_path, arcname=f"files/{os.path.basename(file_path)}"
                    )

    os.remove(kml_file)


def generate_kmz_from_csv(csv_file: str, output_folder: str) -> str:
    """
    Main function to generate a KMZ file from a CSV.
    """
    parent_folder = os.path.join(
        OUTPUT_FOLDER, os.path.splitext(os.path.basename(csv_file))[0]
    )
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)
        logging.info(f"Created directory {parent_folder}")

    df = pd.read_csv(csv_file)

    logging.info(f"Read CSV file: {csv_file}")

    folder_map = {
        "photo_path": os.path.join(parent_folder, PHOTO_FOLDER),
        "icon_url": os.path.join(parent_folder, ICON_FOLDER),
    }

    df = process_media_files(df, folder_map)

    kml_file = os.path.join(parent_folder, "doc.kml")
    folder_name = os.path.splitext(os.path.basename(csv_file))[0]
    create_kml(df, kml_file, folder_name)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = os.path.join(parent_folder, f"output_{timestamp}.kmz")
    create_kmz(kml_file, df, output_file)

    logging.info(f"KMZ file saved: {output_file}")

    return output_file
