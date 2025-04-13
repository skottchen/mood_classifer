import pandas as pd
import requests
import librosa
import io
from tqdm import tqdm

# === Load metadata
df = pd.read_csv("modified_autotagging_moodtheme.tsv", sep="\t")
df = df[['PATH', 'TAGS']]

# # === Clean mood tags
# df['TAGS'] = df['TAGS'].str.replace("mood/theme---", "", regex=False)
# df['TAGS'] = df['TAGS'].apply(lambda x: x.split(','))

# # === Filter for folders 00 to 99
# df = df[df['PATH'].str.slice(0, 2).isin([f"{i:02}" for i in range(100)])]

# # === Feature extractor


# def extract_features_from_url(url):
#     try:
#         r = requests.get(url, timeout=10)
#         y, sr = librosa.load(io.BytesIO(r.content), duration=30)

#         return {
#             'tempo': librosa.beat.tempo(y=y, sr=sr)[0],
#             'zcr': librosa.feature.zero_crossing_rate(y).mean(),
#             'centroid': librosa.feature.spectral_centroid(y=y, sr=sr).mean(),
#         }
#     except Exception as e:
#         print(f"❌ {url} failed: {e}")
#         return None


# # === Loop through all valid URLs
# BASE_URL = "https://cdn.freesound.org/mtg-jamendo/autotagging_moodtheme/audio/"
# features, labels = [], []

# print("🎧 Streaming MP3s from folders 00–99...")
# for _, row in tqdm(df.iterrows(), total=len(df)):
#     url = BASE_URL + row['PATH']
#     feats = extract_features_from_url(url)
#     if feats:
#         features.append(feats)
#         labels.append(row['TAGS'])

# # === Done collecting!
# X = pd.DataFrame(features)
# y = labels

# print(f"✅ Finished: {len(X)} tracks processed")
