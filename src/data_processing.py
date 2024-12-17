import os
import pandas as pd
import logging
from src.exif_operations import get_exif_data, parse_gps_data, format_datetime
from src.file_operations import (
    is_url,
    download_file,
    create_workbook_with_headers,
    save_workbook,
)
from src.config import IMAGE_EXTENSIONS, HEADERS


def process_media_files(df: pd.DataFrame, folder_map: dict) -> pd.DataFrame:
    """
    Download media files (photos and icons) from URLs and update dataframe paths.
    """
    for column, folder in folder_map.items():
        if column not in df:
            continue

        for index, value in df[column].items():
            if pd.notnull(value) and is_url(value):
                local_filename = os.path.join(folder, os.path.basename(value))
                if os.path.exists(local_filename):
                    logging.info(
                        f"File already exists for {column} at index {index}: {local_filename}"
                    )
                    df.at[index, column] = local_filename
                    continue

                local_path = download_file(value, folder)
                if local_path:
                    logging.info(f"Downloaded {column} at index {index}: {value}")
                    df.at[index, column] = local_path
                else:
                    logging.warning(
                        f"Failed to download {column} at index {index}: {value}"
                    )

    return df


def process_image(file_path):
    """Process an image file and extract required data."""
    exif_data = get_exif_data(file_path)
    gps_info = exif_data.get("GPSInfo")
    date_taken = exif_data.get("DateTime")

    lat, lon = parse_gps_data(gps_info)
    date_taken, date_taken_iso = format_datetime(date_taken)

    if lat is not None and lon is not None:
        google_maps_url = f"https://www.google.com/maps?q={lat},{lon}"
        logging.info(
            f"Processed image: {os.path.basename(file_path)} | Coordinates: {lat}, {lon}"
        )
        return {
            "file_name": os.path.basename(file_path),
            "longitude": lon,
            "latitude": lat,
            "maps_url": google_maps_url,
            "date_taken": date_taken,
            "date_taken_iso": date_taken_iso,
            "latlong": f"{lat}, {lon}",
        }
    logging.warning(f"No GPS data found in image: {os.path.basename(file_path)}")
    return None


def process_images_in_folder(folder, worksheet):
    """Process all image files in a folder and append data to the worksheet."""
    logging.info(f"Processing images in folder: {folder}")
    for file_name in os.listdir(folder):
        if file_name.lower().endswith(IMAGE_EXTENSIONS):
            file_path = os.path.join(folder, file_name)
            image_data = process_image(file_path)
            if image_data:
                worksheet.append(
                    [
                        image_data["file_name"],
                        image_data["longitude"],
                        image_data["latitude"],
                        image_data["maps_url"],
                        image_data["date_taken"],
                        image_data["date_taken_iso"],
                        image_data["latlong"],
                    ]
                )


def gps_extraction_logging(output_folder, log_file_name="gps_extraction.log"):
    """Set up logging to log into a file dynamically created in the output folder."""
    log_file_path = os.path.join(output_folder, log_file_name)
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Remove any existing handlers to avoid duplication
    if logger.hasHandlers():
        logger.handlers.clear()

    # File handler - write to log file
    file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    # Console handler - print to terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(file_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.info(f"Logging initialized. Log file: {log_file_path}")


def bulk_gps_extraction(folder, output_folder, excel_name):
    """Main function to process images and export data to Excel."""
    gps_extraction_logging(output_folder)
    workbook, worksheet = create_workbook_with_headers(HEADERS)
    process_images_in_folder(folder, worksheet)
    save_workbook(workbook, output_folder, excel_name)
    logging.info("Image processing workflow completed.")
