"""
Upload Folders to Specific Google Drive Locations using rclone
Author: Juan David Lamus Rincón

This script reads a list of folder names and associated Google Drive links from an Excel file,
then uploads each folder to the correct Drive destination using rclone.

Note: You must configure your rclone remote (e.g. "drive_unidad") before running the script.
"""

import os
import re
import pandas as pd
import subprocess

# Path to the Excel file containing folder codes and Google Drive links
excel_file = "codes_and_links.xlsx"
df = pd.read_excel(excel_file, header=None, dtype=str)

# Local base directory containing folders to upload
base_folder = os.path.join(os.getcwd(), "Downloads")

# Regular expression to extract folder ID from Drive links
drive_id_pattern = re.compile(r"folders/([a-zA-Z0-9_-]+)")

# Track folders that failed to upload
failed_folders = []

# Process each row in the spreadsheet
for _, row in df.iterrows():
    folder_codes = str(row.iloc[0]).strip()
    drive_link = str(row.iloc[1]).strip()

    # Skip rows with invalid codes or empty Drive link
    if not re.match(r"^\d", folder_codes) or pd.isna(drive_link) or drive_link.lower() == "nan":
        continue

    # Extract Drive folder ID
    match = drive_id_pattern.search(drive_link)
    if not match:
        print(f"Could not extract Drive ID from row: {row.values}")
        continue

    drive_id = match.group(1)

    # Support multiple folder codes separated by spaces, commas, or underscores
    split_codes = re.split(r'[,\s_-]+', folder_codes)
    cleaned_codes = [code.split('_')[0] for code in split_codes]

    for code in cleaned_codes:
        local_folder_path = os.path.join(base_folder, code)

        if os.path.exists(local_folder_path):
            num_files = sum(len(files) for _, _, files in os.walk(local_folder_path))

            print(f"\n======================================")
            print(f"📁 Uploading folder: {code}")
            print(f"📂 Local path: {local_folder_path}")
            print(f"📄 Files inside: {num_files}")
            print(f"🎯 Drive destination (ID): {drive_id}")
            print("======================================\n")

            # Build rclone command and execute
            rclone_command = (
                f"rclone copy '{local_folder_path}' drive_unidad: "
                f"--drive-root-folder-id {drive_id} --progress --ignore-existing"
            )

            result = subprocess.run(rclone_command, shell=True)

            if result.returncode != 0:
                print(f"❌ ERROR uploading {code} to {drive_id}.")
                failed_folders.append(code)
            else:
                print(f"✅ Upload completed: {code}")
        else:
            print(f"⚠️ Folder not found: {code}")

# Summary report
print("\n===== SUMMARY =====")
print(f"Folders that failed to upload due to permission issues: {len(failed_folders)}")

if failed_folders:
    print("These folders could not be uploaded:")
    for folder in failed_folders:
        print(f"- {folder}")
else:
    print("✅ All folders uploaded successfully.")

