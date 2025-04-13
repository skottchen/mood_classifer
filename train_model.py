import os
import numpy as np
import pandas as pd
import librosa
from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from concurrent.futures import ThreadPoolExecutor, as_completed
from sklearn.multioutput import MultiOutputClassifier
from collections import Counter
import joblib
MAX_THREADS = 10
MIN_TAG_COUNT = 15

# === Paths
AUDIO_DIR = os.path.join("mtg_jamendo", "autotagging_moodtheme", "audio")
TSV_FILE = "modified_autotagging_moodtheme.tsv"

# === Load metadata
df = pd.read_csv(TSV_FILE, sep="\t")
df['TAGS'] = df['TAGS'].str.replace(
    '{mood/theme: [', '').str.replace(']}', '').str.split(', ')
df['track_id'] = df['TRACK_ID'].astype(str).str.zfill(7)

# === Get list of downloaded .mp3s
downloaded_track_ids = []
for folder in os.listdir(AUDIO_DIR):
    folder_path = os.path.join(AUDIO_DIR, folder)
    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith(".mp3"):
                track_id = "track_" + file.replace(".mp3", "")
                downloaded_track_ids.append(track_id)

df = df[df['track_id'].isin(downloaded_track_ids)]

# === Audio feature extractor
def extract_features_threaded(row):
    """
    Extracts a fixed-length audio feature vector for a given track row using Librosa.

    Parameters:
        row (pandas.Series): A row from the metadata DataFrame containing:
            - 'track_id': the ID of the track (used to locate the .mp3 file)
            - 'PATH': the relative folder path (e.g., '00/')

    Returns:
        tuple:
            - features (np.ndarray): A 38-dimensional numpy array combining MFCC, Chroma, Spectral Contrast, and Tonnetz features.
            - labels (list): The list of mood tags associated with the track.
            If the file is invalid, too short, or an error occurs, returns (None, None).
    """
    try:
        track_id = row['track_id']
        folder = row['PATH'][:2]
        file_path = os.path.join(AUDIO_DIR, folder, f"{track_id}.mp3")
        file_path = file_path.replace("track_", "")

        if not os.path.exists(file_path):
            return None, None

        y, sr = librosa.load(file_path, sr=None, mono=True)
        if librosa.get_duration(y=y, sr=sr) < 30:
            return None, None

        mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1)
        chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr), axis=1)
        contrast = np.mean(
            librosa.feature.spectral_contrast(y=y, sr=sr), axis=1)
        tonnetz = np.mean(librosa.feature.tonnetz(
            y=librosa.effects.harmonic(y), sr=sr), axis=1)

        features = np.concatenate([mfcc, chroma, contrast, tonnetz])
        return features, row['TAGS']
    except Exception as e:
        print(f"⚠️ Failed: {row['track_id']} — {e}")
        return None, None


# === Threaded feature extraction
features = []
labels = []

print(
    f"📁 Extracting features from {len(df)} audio files using {MAX_THREADS} threads...\n")

with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    futures = [executor.submit(extract_features_threaded, row)
               for _, row in df.iterrows()]

    for future in tqdm(as_completed(futures), total=len(futures), desc="🎧 Extracting features"):
        feat, tag = future.result()
        if feat is not None:
            features.append(feat)
            labels.append(tag)

# === Check result
if not features:
    raise ValueError(
        "❌ No valid features extracted. Check audio file quality.")

X = np.array(features)
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(labels)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42)

model = MultiOutputClassifier(
    RandomForestClassifier(
        n_estimators=300,
        max_depth=25,
        min_samples_split=4,
        random_state=42,
        n_jobs=-1
    )
)

model.fit(X_train, y_train)

print("\n📊 Classification Report:\n")
print(classification_report(y_test, model.predict(
    X_test), target_names=mlb.classes_))

# === Save model artifacts
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/mood_model.pkl")
joblib.dump(mlb, "models/label_binarizer.pkl")
joblib.dump(scaler, "models/scaler.pkl")
print("\n✅ Model and preprocessing saved in `models/`.")
