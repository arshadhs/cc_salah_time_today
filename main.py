#!/usr/bin/env python

"""
    Display salah time in pretty format
"""

__author__      = "Arshad H. Siddiqui"
__copyright__   = "MIT license"

import json
from datetime import datetime, timedelta
import re

# File paths
prayer_file = 'time.json'
hadith_file = 'hadith.txt'

# Step 1: Load prayer data from time.json
with open(prayer_file, 'r') as file:
    prayer_data = json.load(file)

# Get today's and tomorrow's dates in "DD MMM" format
today = datetime.now().strftime("%d %b")
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d %b")
day_of_month = int(datetime.now().strftime("%d"))  # Extract the day as an integer

# Find today's and tomorrow's prayer times in the JSON data
today_prayers = next((day for day in prayer_data if day['date'] == today), None)
tomorrow_prayers = next((day for day in prayer_data if day['date'] == tomorrow), None)

# Step 2: Load hadith data, serialize it, and select the hadith based on today's day
with open(hadith_file, 'r') as file:
    hadith_content = file.read()

# Split hadith content by "---" and filter out empty sections
hadith_sections = [section.strip() for section in hadith_content.split('---') if section.strip()]

# Calculate the index for today's hadith
hadith_index = (day_of_month - 1) % len(hadith_sections)  # Wrap around if day exceeds available hadiths
selected_hadith = hadith_sections[hadith_index]

# Remove "Volume..." and "Narrated..." text for cleaner output
trimmed_hadith = re.sub(r'Volume.*?Narrated.*?:\s*', '', selected_hadith, flags=re.DOTALL)

# Helper function to convert time to 12-hour format with a.m./p.m.
def to_12hr_format(time_str):
    return datetime.strptime(time_str, "%H:%M").strftime("%I:%M %p").lstrip("0").replace("AM", "a.m.").replace("PM", "p.m.")

# Step 3: Print prayer times and selected hadith
if today_prayers and tomorrow_prayers:
    # Extract today's Maghrib and Isha, and tomorrow's Fajr details
    maghrib = next((namaz for namaz in today_prayers['namaz'] if namaz['name'].lower() == 'magrib'), None)
    isha = next((namaz for namaz in today_prayers['namaz'] if namaz['name'].lower() == 'isha'), None)
    fajr_tomorrow = next((namaz for namaz in tomorrow_prayers['namaz'] if namaz['name'].lower() == 'fajr'), None)

    # Print the results in the specified format if found
    if maghrib and isha and fajr_tomorrow:
        print(f"Magrib {to_12hr_format(maghrib['jamat'])} {maghrib['loc']}")
        print(f"Isha {to_12hr_format(isha['jamat'])} {isha['loc']}")
        print(f"Fajr {to_12hr_format(fajr_tomorrow['jamat'])} {fajr_tomorrow['loc']}")
    else:
        print("Prayer times for Fajr, Maghrib, or Isha are missing in today's or tomorrow's data.")
else:
    print("Today's or tomorrow's date not found in the prayer times data.")

# Print a line break, the formatted hadith with --- before and after, and the URL
print("\n---")
print(trimmed_hadith.strip())
print("---\n")
print("https://www.cambournecrescent.org/prayer")