from pathlib import Path
import wfdb
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

# 1) اعثر على ملف RECORDS تلقائيًا
records_files = list((BASE_DIR / "data").rglob("RECORDS"))
if not records_files:
    raise FileNotFoundError("لم يتم العثور على ملف RECORDS داخل مجلد data.")

records_path = records_files[0]
DATA_DIR = records_path.parent

print("Using DATA_DIR:", DATA_DIR)

# 2) اقرأ أسماء كل التسجيلات
with open(records_path, "r", encoding="utf-8") as f:
    record_names = [line.strip() for line in f if line.strip()]

print("Total records:", len(record_names))

def extract_features(sig: np.ndarray, fs: int) -> dict:
    """Features بسيطة وسريعة (قابلة للتطوير لاحقًا)."""
    x = sig.squeeze().astype(float)
    x = np.nan_to_num(x)

    feats = {
        "mean": float(np.mean(x)),
        "std": float(np.std(x)),
        "min": float(np.min(x)),
        "max": float(np.max(x)),
        "median": float(np.median(x)),
        "rms": float(np.sqrt(np.mean(x**2))),
        "energy": float(np.sum(x**2)),
        "zcr": float(np.mean(np.abs(np.diff(np.sign(x))) > 0)),
        "duration_sec": float(len(x) / fs),
        "fs": int(fs),
        "n_samples": int(len(x)),
    }
    return feats

rows = []
for i, rec_name in enumerate(record_names, start=1):
    rec = wfdb.rdrecord(str(DATA_DIR / rec_name))
    sig = rec.p_signal
    fs = int(rec.fs)

    feats = extract_features(sig, fs)
    feats["record"] = rec_name

    # 3) (اختياري) حاول نقرأ label من ملف txt إذا موجود
    txt_path = DATA_DIR / f"{rec_name}.txt"
    if txt_path.exists():
        txt = txt_path.read_text(encoding="utf-8", errors="ignore")
        feats["meta_text"] = txt[:200].replace("\n", " ").replace("\r", " ")  # أول 200 حرف فقط
    else:
        feats["meta_text"] = ""

    rows.append(feats)

    if i % 20 == 0 or i == len(record_names):
        print(f"Processed {i}/{len(record_names)}")

df = pd.DataFrame(rows)

out_csv = BASE_DIR / "physionet_features.csv"
df.to_csv(out_csv, index=False)

print("\n✅ Saved:", out_csv)
print("Shape:", df.shape)
print(df.head())
