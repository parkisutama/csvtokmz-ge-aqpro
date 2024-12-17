from datetime import datetime
from PIL import Image, ExifTags


def get_exif_data(image_path):
    """Extract EXIF data from an image."""
    image = Image.open(image_path)
    exif_raw = image._getexif()
    return (
        {ExifTags.TAGS[k]: v for k, v in exif_raw.items() if k in ExifTags.TAGS}
        if exif_raw
        else {}
    )


# Convert GPS coordinates from degrees, minutes, and seconds to decimal degrees
def convert_to_degrees(value):
    """Convert GPS coordinates from degrees, minutes, and seconds to decimal degrees."""
    d, m, s = float(value[0]), float(value[1]), float(value[2])
    return d + (m / 60.0) + (s / 3600.0)


def extract_gps_info(image_path: str) -> tuple:
    """Extract GPS information from an image."""
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data is not None:
            for tag, value in exif_data.items():
                decoded = ExifTags.TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_info = {ExifTags.GPSTAGS.get(t, t): v for t, v in value.items()}
                    latitude = convert_to_degrees(gps_info.get("GPSLatitude"))
                    longitude = convert_to_degrees(gps_info.get("GPSLongitude"))
                    return (longitude, latitude)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
    return (None, None)


def parse_gps_data(gps_info):
    """Extract latitude and longitude from GPS EXIF data."""
    if not gps_info:
        return None, None

    lat = convert_to_degrees(gps_info[2])
    lon = convert_to_degrees(gps_info[4])

    # Adjust for hemisphere
    lat = -lat if gps_info[1] == "S" else lat
    lon = -lon if gps_info[3] == "W" else lon
    return lat, lon


def format_datetime(exif_date):
    """Format EXIF DateTime to human-readable and ISO8601 formats."""
    if not exif_date:
        return "N/A", "N/A"

    try:
        dt = datetime.strptime(exif_date, "%Y:%m:%d %H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M:%S"), dt.strftime("%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return "Invalid Format", "Invalid Format"
