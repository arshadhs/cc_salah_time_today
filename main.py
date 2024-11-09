import json
import random
from datetime import datetime

# File paths
prayer_file = 'time.json'
hadith_file = 'hadith.txt'

# Step 1: Load prayer data from time.json
with open(prayer_file, 'r') as file:
    prayer_data = json.load(file)

# Get today's date in "DD MMM" format
today = datetime.now().strftime("%d %b")

# Find today's prayer times in the JSON data
today_prayers = next((day for day in prayer_data if day['date'] == today), None)

# Step 2: Load hadith data and select a random section
with open(hadith_file, 'r') as file:
    hadith_content = file.read()

# Split the hadith content by "---" and filter out empty sections
hadith_sections = [section.strip() for section in hadith_content.split('---') if section.strip()]
random_hadith = random.choice(hadith_sections) if hadith_sections else "No hadith available."

# Step 3: Print prayer times and selected hadith
if today_prayers:
    # Extract Fajr, Maghrib, and Isha details
    fajr = next((namaz for namaz in today_prayers['namaz'] if namaz['name'].lower() == 'fajr'), None)
    maghrib = next((namaz for namaz in today_prayers['namaz'] if namaz['name'].lower() == 'magrib'), None)
    isha = next((namaz for namaz in today_prayers['namaz'] if namaz['name'].lower() == 'isha'), None)

    # Print the results in the specified format if found
    if maghrib and isha and fajr:
        print(f"Magrib {maghrib['jamat']} {maghrib['loc']}")
        print(f"Isha {isha['jamat']} {isha['loc']}")
        print(f"Fajr {fajr['jamat']} {fajr['loc']}")
    else:
        print("Prayer times for Fajr, Maghrib, or Isha are missing in today's data.")
else:
    print("Today's date not found in the prayer times data.")

# Print a line break, the random hadith, another line break, and the URL
print("\n" + --- + "\n")
print("\n" + random_hadith + "\n")
print("\n" + --- + "\n")
print("https://www.cambournecrescent.org/prayer")
