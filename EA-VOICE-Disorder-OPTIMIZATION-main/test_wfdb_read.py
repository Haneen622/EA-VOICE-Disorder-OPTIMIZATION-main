from pathlib import Path
import wfdb

BASE_DIR = Path(__file__).resolve().parent

records_files = list((BASE_DIR / "data").rglob("RECORDS"))

print("BASE_DIR:", BASE_DIR)
print("Found RECORDS files:", len(records_files))

if not records_files:
    raise FileNotFoundError("لم يتم العثور على ملف RECORDS داخل مجلد data.")

records_path = records_files[0]
DATA_DIR = records_path.parent

print("Using DATA_DIR:", DATA_DIR)
print("RECORDS path:", records_path)

with open(records_path, "r", encoding="utf-8") as f:
    first_record = f.readline().strip()

print("First record:", first_record)

# ✅ قراءة محلية (بدون pn_dir)
rec = wfdb.rdrecord(str(DATA_DIR / first_record))

print("Signal shape:", rec.p_signal.shape)
print("Sampling rate:", rec.fs)
