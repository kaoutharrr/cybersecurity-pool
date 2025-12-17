#!/usr/bin/env python3
import sys
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime

ALLOWED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp")

def is_supported(filepath: str) -> bool:
    return filepath.lower().endswith(ALLOWED_EXTENSIONS)

def get_file_info(filepath: str) -> dict:
    """Get basic file information"""
    stats = os.stat(filepath)
    return {
        "Filename": os.path.basename(filepath),
        "File Size": f"{stats.st_size:,} bytes",
        "Created": datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
        "Modified": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
    }

def get_image_info(img: Image.Image) -> dict:
    """Get basic image properties"""
    return {
        "Format": img.format,
        "Mode": img.mode,
        "Size": f"{img.size[0]} x {img.size[1]} pixels",
    }

def convert_gps_to_degrees(value, ref):
    """Convert GPS coordinates to decimal degrees"""
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])
    decimal = d + (m / 60.0) + (s / 3600.0)
    if ref in ["S", "W"]:
        decimal = -decimal
    return decimal

def parse_gps(gps_data: dict) -> dict:
    """Parse GPS information from EXIF"""
    gps_info = {}
    try:
        if "GPSLatitude" in gps_data and "GPSLatitudeRef" in gps_data:
            lat = convert_gps_to_degrees(
                gps_data["GPSLatitude"],
                gps_data["GPSLatitudeRef"]
            )
            gps_info["Latitude"] = f"{lat:.6f}"
        
        if "GPSLongitude" in gps_data and "GPSLongitudeRef" in gps_data:
            lon = convert_gps_to_degrees(
                gps_data["GPSLongitude"],
                gps_data["GPSLongitudeRef"]
            )
            gps_info["Longitude"] = f"{lon:.6f}"
        
        if "Latitude" in gps_info and "Longitude" in gps_info:
            gps_info["Maps URL"] = f"https://maps.google.com/?q={lat},{lon}"
        
        if "GPSAltitude" in gps_data:
            gps_info["Altitude"] = f"{float(gps_data['GPSAltitude']):.2f}m"
        
        if "GPSDateStamp" in gps_data:
            gps_info["GPS Date"] = gps_data["GPSDateStamp"]
    except Exception:
        pass
    
    return gps_info

def get_exif_data(img: Image.Image) -> dict:
    """Extract EXIF metadata from image"""
    exif_data = {}
    
    try:
        exif_raw = img._getexif()
        if exif_raw is None:
            return {}
        
        for tag_id, value in exif_raw.items():
            tag_name = TAGS.get(tag_id, tag_id)

            if tag_name == "GPSInfo":
                gps_raw = {}
                for gps_id, gps_val in value.items():
                    gps_tag = GPSTAGS.get(gps_id, gps_id)
                    gps_raw[gps_tag] = gps_val
                gps_parsed = parse_gps(gps_raw)
                if gps_parsed:
                    exif_data["GPS"] = gps_parsed
            
            
            elif isinstance(value, bytes):
                try:
                    exif_data[tag_name] = value.decode("utf-8", errors="ignore")
                except:
                    exif_data[tag_name] = "<binary>"
            else:
                exif_data[tag_name] = value
    
    except AttributeError:
       
        pass
    except Exception:
        pass
    
    return exif_data

def display_metadata(filepath: str):
    """Display all metadata for an image file"""
    print("\n" + "=" * 70)
    print(f"FILE: {filepath}")
    print("=" * 70)
    
    if not os.path.exists(filepath):
        print("[!] Error: File not found")
        return
    
    if not is_supported(filepath):
        print(f"[!] Error: Unsupported format")
        print(f"    Supported: {', '.join(ALLOWED_EXTENSIONS)}")
        return
    
    try:
        # File information
        print("\n📄 FILE INFORMATION")
        print("-" * 70)
        file_info = get_file_info(filepath)
        for key, value in file_info.items():
            print(f"  {key:20} : {value}")
        
        # Open image
        img = Image.open(filepath)
        
        # Image properties
        print("\n🖼️  IMAGE PROPERTIES")
        print("-" * 70)
        img_info = get_image_info(img)
        for key, value in img_info.items():
            print(f"  {key:20} : {value}")
        
        # EXIF data
        exif_data = get_exif_data(img)
        
        if exif_data:
            print("\n📷 EXIF METADATA")
            print("-" * 70)
            
            # Important fields first
            important = [
                "DateTime", "DateTimeOriginal", "DateTimeDigitized",
                "Make", "Model", "Software",
                "ExposureTime", "FNumber", "ISOSpeedRatings", "FocalLength",
                "Artist", "Copyright"
            ]
            
            displayed = set()
            for field in important:
                if field in exif_data:
                    value = exif_data[field]
                    print(f"  {field:20} : {value}")
                    displayed.add(field)
            
            # GPS data
            if "GPS" in exif_data:
                print("\n📍 GPS LOCATION")
                print("-" * 70)
                for key, value in exif_data["GPS"].items():
                    print(f"  {key:20} : {value}")
                displayed.add("GPS")
            
            # Other EXIF fields
            other = {k: v for k, v in exif_data.items() if k not in displayed}
            if other:
                print("\n📋 OTHER METADATA")
                print("-" * 70)
                for key, value in sorted(other.items()):
                    val_str = str(value)
                    if len(val_str) > 50:
                        val_str = val_str[:47] + "..."
                    print(f"  {key:20} : {val_str}")
        else:
            print("\n[i] No EXIF data found")
        
        img.close()
        
    except Exception as e:
        print(f"[!] Error: {e}")
    
    print("=" * 70)

def main():
    if len(sys.argv) < 2:
        print("Usage: ./scorpion.py FILE1 [FILE2 ...]")
        print("\nDisplays metadata and EXIF information from image files")
        print(f"Supported formats: {', '.join(ALLOWED_EXTENSIONS)}")
        sys.exit(1)
    
    files = sys.argv[1:]
    
    print("=" * 70)
    print("SCORPION - Image Metadata Viewer")
    print("=" * 70)
    print(f"Processing {len(files)} file(s)...")
    
    for filepath in files:
        display_metadata(filepath)
    
    print("\n✓ Complete!\n")

if __name__ == "__main__":
    main()