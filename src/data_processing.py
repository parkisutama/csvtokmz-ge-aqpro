import os
import pandas as pd
import logging
from src.file_operations import is_url, download_file


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
