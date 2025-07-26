# ☁️ Google Drive Folder Uploader using rclone

This script automates the upload of multiple local folders to their respective Google Drive destinations using [rclone](https://rclone.org/).

It reads folder codes and Google Drive links from an Excel file and uses `rclone copy` to upload each folder to the appropriate Drive folder ID.

---

## 📄 Features

- Reads from an Excel sheet with:
  - Column 1: Folder codes (can be multiple per cell)
  - Column 2: Google Drive folder links
- Automatically extracts Drive folder IDs
- Skips invalid rows and reports failures
- Displays summary at the end

---

## 📦 Requirements

- Python 3.8+
- [rclone](https://rclone.org/downloads/) installed and configured
- An rclone remote named `drive_unidad` (or change it in the script)
- Excel file with folder codes and links (e.g. `codes_and_links.xlsx`)

Install Python dependencies:

```bash
pip install pandas openpyxl

