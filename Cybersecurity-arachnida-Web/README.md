# Arachnida Project - Complete Beginner's Guide 🕷️

## Table of Contents
1. [What is Cybersecurity?](#what-is-cybersecurity)
2. [Project Overview](#project-overview)
3. [Key Concepts Explained](#key-concepts-explained)
4. [Prerequisites](#prerequisites)
5. [Program 1: Spider - Web Scraper](#program-1-spider)
6. [Program 2: Scorpion - Metadata Analyzer](#program-2-scorpion)
7. [Step-by-Step Implementation Guide](#implementation-guide)
8. [Common Challenges & Solutions](#common-challenges)
9. [Resources](#resources)

---

## What is Cybersecurity?

**Cybersecurity** is the practice of protecting computer systems, networks, and data from digital attacks, unauthorized access, or damage. It's like being a digital security guard.

### Why Does This Project Matter?

This project teaches you two important security concepts:
- **Web scraping**: Understanding how automated tools can extract data from websites (important for both attackers and defenders)
- **Metadata analysis**: Learning what hidden information exists in files and how it can compromise privacy

---

## Project Overview

You'll build **TWO programs**:

| Program | Purpose | What It Does |
|---------|---------|--------------|
| **Spider** 🕷️ | Web Scraper | Downloads images from websites automatically |
| **Scorpion** 🦂 | Metadata Analyzer | Reads and displays hidden information in images |

---

## Key Concepts Explained

### 1. Web Scraping
**What is it?** Automatically extracting data from websites using code instead of manually clicking and downloading.

**Real-world example:** Google's search engine uses web scraping to index the entire internet!

**In this project:** Your spider program visits a website, finds all image links, and downloads them.

### 2. Recursion
**What is it?** When something refers to itself. In web scraping, it means following links to other pages.

**Example:**
```
You visit: example.com
  ↓ Find link to: example.com/gallery
    ↓ Find link to: example.com/gallery/2024
      ↓ Download images from each page
```

**Depth level:** How many "layers" deep you go. Level 1 = just the main page. Level 5 = follow links 5 times.

### 3. Metadata
**What is it?** Data about data. Hidden information stored inside files.

**Photo metadata might include:**
- When the photo was taken
- What camera/phone was used
- GPS coordinates (where it was taken!)
- Who edited it
- Software used

**Why it matters:** This information can accidentally reveal:
- Your location
- Your daily routine
- What devices you own
- When you're home or away

### 4. EXIF Data
**EXIF** = Exchangeable Image File Format

This is a specific type of metadata for images. It's like a secret note attached to every photo that contains technical details.

---

## Prerequisites

### Programming Knowledge
You need to know **one programming language**. Best choices:
- **Python** (recommended - easiest for beginners)
- Ruby
- JavaScript (Node.js)
- Go
- Any language you're comfortable with

### Concepts You Should Understand
- Variables and data types
- Functions
- Loops (for, while)
- Conditional statements (if/else)
- File operations (reading/writing files)
- Basic command-line usage

### Don't Know Programming Yet?
Start here:
1. Learn Python basics (2-3 weeks): [Python.org Tutorial](https://docs.python.org/3/tutorial/)
2. Practice on [Codecademy](https://www.codecademy.com/learn/learn-python-3) or [freeCodeCamp](https://www.freecodecamp.org/)

---

## Program 1: Spider

### What It Does
Downloads all images from a website (and optionally follows links to other pages).

### Command Format
```bash
./spider [-rlp] URL
```

### Options Explained

| Option | Description | Example |
|--------|-------------|---------|
| `-r` | Recursive mode (follow links) | `./spider -r https://example.com` |
| `-l [N]` | Maximum depth (default: 5) | `./spider -r -l 3 https://example.com` |
| `-p [PATH]` | Save location (default: ./data/) | `./spider -p /tmp/images https://example.com` |

### Supported Image Types
- `.jpg` / `.jpeg`
- `.png`
- `.gif`
- `.bmp`

### How It Works (Step-by-Step)

1. **Receive URL** from command line
2. **Download the webpage** HTML content
3. **Parse HTML** to find all image links
4. **Download each image** and save to disk
5. **If recursive mode:** Find all links on the page
6. **Follow each link** (up to max depth) and repeat steps 2-5
7. **Keep track** of visited URLs (don't visit the same page twice)

### Example Usage
```bash
# Simple download - just images on the main page
./spider https://example.com/gallery

# Recursive download - follow links 2 levels deep
./spider -r -l 2 https://example.com/gallery

# Custom save location
./spider -r -p ~/Downloads/gallery https://example.com/gallery
```

---

## Program 2: Scorpion

### What It Does
Analyzes image files and displays their hidden metadata.

### Command Format
```bash
./scorpion FILE1 [FILE2 ...]
```

### What It Should Display
- **Basic info**: File size, creation date, modification date
- **EXIF data**: Camera model, GPS coordinates, ISO, aperture, etc.
- **Other metadata**: Software used, author, copyright

### Example Usage
```bash
# Analyze one file
./scorpion photo.jpg

# Analyze multiple files
./scorpion photo1.jpg photo2.png photo3.gif
```

### Example Output
```
File: photo.jpg
========================================
Basic Information:
  - File Size: 2.3 MB
  - Created: 2024-03-15 14:23:11
  - Modified: 2024-03-15 14:23:11

EXIF Data:
  - Camera Make: Apple
  - Camera Model: iPhone 13 Pro
  - Date Taken: 2024-03-15 14:23:11
  - GPS Latitude: 37.7749° N
  - GPS Longitude: 122.4194° W
  - ISO: 64
  - Aperture: f/1.5
  - Focal Length: 26mm
```

---

## Implementation Guide

### Phase 1: Spider (Week 1-2)

#### Step 1: Set Up Your Project
```bash
# Create project structure
mkdir arachnida
cd arachnida
mkdir spider scorpion data
```

#### Step 2: Learn HTTP Requests
You need to download web pages. In Python:
```python
import requests

response = requests.get('https://example.com')
html_content = response.text
```

#### Step 3: Learn HTML Parsing
Find image links in HTML. In Python:
```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_content, 'html.parser')
images = soup.find_all('img')

for img in images:
    img_url = img.get('src')
    print(img_url)
```

#### Step 4: Download Images
```python
import requests

def download_image(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)
```

#### Step 5: Add Command-Line Arguments
```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('url', help='URL to scrape')
parser.add_argument('-r', action='store_true', help='Recursive mode')
parser.add_argument('-l', type=int, default=5, help='Max depth')
parser.add_argument('-p', default='./data/', help='Save path')

args = parser.parse_args()
```

#### Step 6: Implement Recursion
Keep track of:
- Current depth level
- Visited URLs (use a set)
- Queue of URLs to visit

Pseudocode:
```
visited = set()
to_visit = [(start_url, 0)]  # (url, depth)

while to_visit is not empty:
    current_url, depth = to_visit.pop()
    
    if current_url in visited:
        continue
    
    if depth > max_depth:
        continue
    
    visited.add(current_url)
    
    # Download images from current_url
    # Find all links on current_url
    # Add new links to to_visit with depth+1
```

### Phase 2: Scorpion (Week 3)

#### Step 1: Learn File Reading
```python
with open('image.jpg', 'rb') as f:
    image_data = f.read()
```

#### Step 2: Extract Basic Metadata
```python
import os
from datetime import datetime

file_stats = os.stat('image.jpg')
size = file_stats.st_size
created = datetime.fromtimestamp(file_stats.st_ctime)
modified = datetime.fromtimestamp(file_stats.st_mtime)
```

#### Step 3: Extract EXIF Data
In Python, use the PIL/Pillow library:
```python
from PIL import Image
from PIL.ExifTags import TAGS

image = Image.open('photo.jpg')
exif_data = image._getexif()

if exif_data:
    for tag_id, value in exif_data.items():
        tag_name = TAGS.get(tag_id, tag_id)
        print(f"{tag_name}: {value}")
```

#### Step 4: Handle Different File Types
Each image format stores metadata differently:
- **JPEG**: Uses EXIF
- **PNG**: Uses text chunks
- **GIF**: Limited metadata
- **BMP**: Very basic metadata

#### Step 5: Format Output Nicely
Create readable output with sections and proper formatting.

---

## Common Challenges & Solutions

### Challenge 1: Relative vs Absolute URLs
**Problem:** Image links might be relative (`/images/photo.jpg`) instead of absolute (`https://example.com/images/photo.jpg`)

**Solution:** Convert relative URLs to absolute:
```python
from urllib.parse import urljoin

absolute_url = urljoin(base_url, relative_url)
```

### Challenge 2: Handling Errors
**Problem:** Websites might be down, images might not exist, etc.

**Solution:** Use try-except blocks:
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error downloading {url}: {e}")
```

### Challenge 3: Avoiding Infinite Loops
**Problem:** Websites might link to each other in circles

**Solution:** Always track visited URLs:
```python
visited = set()

if url not in visited:
    visited.add(url)
    # Process URL
```

### Challenge 4: No EXIF Data
**Problem:** Not all images have EXIF data

**Solution:** Check if data exists before displaying:
```python
exif_data = image._getexif()
if exif_data:
    # Display EXIF
else:
    print("No EXIF data found")
```

### Challenge 5: Permission Issues
**Problem:** Can't create directories or save files

**Solution:** Check and create directories:
```python
import os

if not os.path.exists(save_path):
    os.makedirs(save_path)
```

---

## Important Rules (Don't Get a Zero!)

### ❌ DO NOT USE:
- `wget` command
- `scrapy` library
- Any tool that does web scraping for you

### ✅ YOU CAN USE:
- Libraries for HTTP requests (`requests`, `urllib`, `http.client`)
- Libraries for parsing HTML (`BeautifulSoup`, `lxml`, HTML parsers)
- Libraries for reading metadata (`PIL/Pillow`, `exifread`)
- File handling libraries

### Why?
You need to understand **how** scraping works, not just use a tool that does it for you.

---

## Testing Your Programs

### Test Spider
1. Start with a simple page with 2-3 images
2. Test without recursion first
3. Test with recursion depth 1
4. Test with custom save path
5. Test with a real website (be respectful!)

### Test Scorpion
1. Take photos with your phone (they have EXIF)
2. Download sample images from the internet
3. Test with images that have no metadata
4. Test with multiple file types

---

## Resources

### Learning Python
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/)
- [Automate the Boring Stuff](https://automatetheboringstuff.com/)

### HTTP & Web Scraping
- [Requests Library Documentation](https://requests.readthedocs.io/)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

### Metadata & EXIF
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [EXIF Tags Reference](https://exiftool.org/TagNames/EXIF.html)

### Command-Line Arguments
- [argparse Tutorial](https://docs.python.org/3/howto/argparse.html)

### General Cybersecurity
- [OverTheWire Wargames](https://overthewire.org/) - Practice hacking challenges
- [Cybrary](https://www.cybrary.it/) - Free cybersecurity courses

---

## Project Timeline

### Week 1: Spider Basics
- Set up environment
- Learn HTTP requests
- Download images from single page
- Add command-line arguments

### Week 2: Spider Recursion
- Implement link finding
- Add recursion logic
- Handle errors
- Test thoroughly

### Week 3: Scorpion
- Read file metadata
- Extract EXIF data
- Format output
- Handle different file types

### Week 4: Polish & Bonus
- Code cleanup
- Better error messages
- Documentation
- Bonus features (if time)

---

## Tips for Success

1. **Start simple** - Get basic version working first
2. **Test often** - Don't write 100 lines before testing
3. **Google is your friend** - Everyone looks up syntax
4. **Read error messages** - They usually tell you what's wrong
5. **Ask for help** - Your peers are learning too
6. **Comment your code** - Future you will thank you
7. **Use version control** - Commit often with git

---

## Glossary

- **URL**: Web address (e.g., https://example.com)
- **HTML**: Language that web pages are written in
- **HTTP**: Protocol for transferring web pages
- **Parsing**: Analyzing and extracting information from text
- **Recursion**: When something calls itself
- **Metadata**: Data about data
- **EXIF**: Photo metadata standard
- **CLI**: Command-Line Interface
- **Argument**: Input to a program (like `-r` or `-l 5`)

---

## Final Thoughts

This project might seem overwhelming, but break it down into small steps. Focus on getting one piece working at a time. Remember: every cybersecurity expert started exactly where you are now!

Good luck! 🚀

---

**Questions?** Review this guide, search online, or ask your peers. You've got this!