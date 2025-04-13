import os
import requests
import zipfile

# URL of the zip file
ZIP_URL = "https://zenodo.org/records/3826813/files/data.zip"

# Local paths
ZIP_PATH = "data.zip"
EXTRACT_DIR = "mtg_jamendo"

def download_zip(url, output_path):
    print(f"⬇️ Downloading from {url}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Downloaded: {output_path}")
    else:
        raise Exception(f"❌ Failed to download file: HTTP {response.status_code}")

def extract_zip(zip_path, extract_to):
    print(f"📂 Extracting {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"✅ Extracted to: {extract_to}")

def main():
    if not os.path.exists(ZIP_PATH):
        download_zip(ZIP_URL, ZIP_PATH)
    else:
        print(f"📦 Already downloaded: {ZIP_PATH}")
    
    os.makedirs(EXTRACT_DIR, exist_ok=True)
    extract_zip(ZIP_PATH, EXTRACT_DIR)

if __name__ == "__main__":
    main()
