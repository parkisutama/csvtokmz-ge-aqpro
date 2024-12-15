import os
import requests
import logging


def is_url(path: str) -> bool:
    """Check if a path is a valid URL."""
    return path.startswith(("http://", "https://"))


def download_file(url: str, folder: str) -> str:
    """
    Download a file from a URL and save it locally.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
        logging.info(f"Created folder: {folder}")
    local_filename = os.path.join(folder, os.path.basename(url))

    headers = {"User-Agent": "MyApp/1.0 (example@example.com)"}
    try:
        with requests.get(url, headers=headers, stream=True) as response:
            response.raise_for_status()
            with open(local_filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
    except requests.RequestException as e:
        logging.warning(f"Error downloading {url}: {e}")
        return None

    return local_filename
