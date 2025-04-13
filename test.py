import os
import pandas as pd

# === Paths
AUDIO_DIR = os.path.join("mtg_jamendo", "autotagging_moodtheme", "audio")
INPUT_TSV = "modified_autotagging_moodtheme.tsv"
OUTPUT_TSV = "training_autotagging_moodtheme.tsv"

# === Load the metadata file
df = pd.read_csv(INPUT_TSV, sep="\t")
df['track_id'] = df['TRACK_ID'].astype(str).str.zfill(7)

# === Check which audio files actually exist
existing_ids = []

for folder in os.listdir(AUDIO_DIR):
    folder_path = os.path.join(AUDIO_DIR, folder)
    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith(".mp3"):
                track_id = "track_" + file.replace(".mp3", "")
                existing_ids.append(track_id)

# === Filter metadata to only include downloaded audio files
filtered_df = df[df['track_id'].isin(existing_ids)]

# === Save to new TSV
filtered_df.drop(columns=["track_id"]).to_csv(
    OUTPUT_TSV, sep="\t", index=False)
print(f"✅ Saved {len(filtered_df)} rows to {OUTPUT_TSV}")
