import sys
import os
import magic
import pyfiglet

result = pyfiglet.figlet_format("MetaSmash")
print(result)

print('				   		   By Aardwolf Security\n\n')

try:
    import exiftool
except ImportError:
    print("Error: The 'exiftool' module is not installed.")
    choice = input("Would you like to install it now? (y/n) ")
    if choice.lower() == "y":
        os.system("pip install exiftool")
        import exiftool
    else:
        sys.exit()

try:
    import PIL.ExifTags
    import PIL.Image
except ImportError:
    print("Error: The 'Pillow' module is not installed.")
    choice = input("Would you like to install it now? (y/n) ")
    if choice.lower() == "y":
        os.system("pip install Pillow")
        import PIL.ExifTags
        import PIL.Image
    else:
        sys.exit()

SENSITIVE_TAGS = [
    "EXIF:GPSLatitude",
    "EXIF:GPSLongitude",
    "EXIF:GPSAltitude",
    "EXIF:GPSImgDirection",
    "EXIF:GPSDestLatitude",
    "EXIF:GPSDestLongitude",
    "EXIF:GPSDestBearing",
    "EXIF:GPSDateStamp",
    "EXIF:GPSDifferential",
    "EXIF:GPSHPositioningError",
    "EXIF:UserComment"
]

def extract_metadata(file_path, extract_gps=False):
    """
    Extracts metadata and exif data from a media file.
    """
    with exiftool.ExifTool() as et:
        if extract_gps:
            metadata = et.get_metadata(file_path, SENSITIVE_TAGS)
        else:
            metadata = et.get_metadata(file_path)
    return metadata

def format_metadata(metadata):
    """
    Formats metadata output to be more human-readable.
    """
    formatted_metadata = ""
    for key, value in metadata.items():
        if key in SENSITIVE_TAGS:
            formatted_key = key.replace(":", " ").title()
            formatted_value = str(value).replace("\\n", "\n")
            formatted_metadata += f"{formatted_key}: {formatted_value}\n"
    if not formatted_metadata:
        formatted_metadata = "No sensitive metadata found."
    return formatted_metadata

def main():
    """
    Prompts the user for a file location and extracts sensitive metadata and exif data.
    """
    if len(sys.argv) < 2:
        file_path = input("Please enter a file location: ")
    else:
        file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        print(f"Error: {file_path} is not a valid file.")
        return

    extract_gps = False
    if len(sys.argv) >= 3 and sys.argv[2].lower() == "--gps":
        extract_gps = True

    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)

    if "image" in file_type or "pdf" in file_type or "video" in file_type or "audio" in file_type or "ms-office" in file_type:
        metadata = extract_metadata(file_path, extract_gps)
        formatted_metadata = format_metadata(metadata)
        print(formatted_metadata)
    else:
        print(f"Error: {file_type} is not a supported file type.")

if __name__ == "__main__":
    main()
