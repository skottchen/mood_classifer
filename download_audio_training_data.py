import os
import csv
import random
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

BASE_URL = "https://cdn.freesound.org/mtg-jamendo/autotagging_moodtheme/audio"
TSV_FILE = "modified_autotagging_moodtheme.tsv"
DEST_BASE = os.path.join("mtg_jamendo", "autotagging_moodtheme", "audio")
MAX_THREADS = 8
DOWNLOAD_LIMIT = 1000


def download_mp3(path):
    folder_num = path[:2]
    file_name = path.split("/")[1]
    url = f"{BASE_URL}/{path}"

    dest_folder = os.path.join(DEST_BASE, folder_num)
    os.makedirs(dest_folder, exist_ok=True)
    dest_path = os.path.join(dest_folder, file_name)

    if os.path.exists(dest_path):
        return f"⏭️ Already exists: {file_name}"

    try:
        response = requests.get(url, stream=True, timeout=15)
        if response.status_code == 200:
            with open(dest_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return f"✅ Downloaded: {file_name}"
        else:
            return f"❌ Not found: {url} (HTTP {response.status_code})"
    except Exception as e:
        return f"❌ Error downloading {file_name}: {e}"


# === Load and randomly sample 1000 paths
paths = []
with open(TSV_FILE, "r", encoding="utf-8") as file:
    reader = csv.reader(file, delimiter='\t')
    next(reader)
    for row in reader:
        paths.append(row[3])  # e.g. '00/003456.mp3'

sampled_paths = random.sample(paths, DOWNLOAD_LIMIT)

# === Parallel download with progress bar
print(
    f"🚀 Downloading {DOWNLOAD_LIMIT} random audio files with {MAX_THREADS} threads...\n")

with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    futures = {executor.submit(download_mp3, path)
                               : path for path in sampled_paths}
    for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading"):
        print(future.result())

print("\n✅ Downloads finished.")
