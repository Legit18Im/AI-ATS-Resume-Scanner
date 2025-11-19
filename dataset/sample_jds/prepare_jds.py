# prepare_jds.py
import pandas as pd
import os
import re

# CONFIGURATION
csv_filename = "D:\Team_Project\ATS Scanner\dataset\sample_jds\jobs.csv"  # Make sure this matches your downloaded file
output_dir = "D:\Team_Project\ATS Scanner\dataset\sample_jds"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

try:
    print(f"Reading {csv_filename}...")
    df = pd.read_csv(csv_filename)
    
    # Loop through the first 50 rows to keep it fast
    count = 0
    for index, row in df.head(50).iterrows():
        # Get title and description (handle different column names safely)
        title = str(row.get('Job Title', row.get('title', f"Job_{index}")))
        desc = str(row.get('Job Description', row.get('description', '')))
        
        # Only save if description is long enough
        if len(desc) > 50:
            # Create a clean filename (e.g., "Senior_Python_Developer.txt")
            safe_title = re.sub(r'[^a-zA-Z0-9]', '_', title)[:50]
            filename = f"{safe_title}.txt"
            
            # Write to file
            with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
                f.write(desc)
            count += 1
            
    print(f"✅ Success! Created {count} job files in '{output_dir}'")

except FileNotFoundError:
    print(f"❌ Error: Could not find '{csv_filename}'. Please check the filename.")
except Exception as e:
    print(f"❌ Error: {e}")