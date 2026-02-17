from pathlib import Path
import pandas as pd
import re

BASE_DIR = Path(__file__).resolve().parent
TSV_PATH = BASE_DIR / "data" / "svd_handcrafted_data.tsv"

# 1) اعثر على DATA_DIR الحقيقي من خلال RECORDS (نفس مجلد voiceXXX.*)
records_files = list((BASE_DIR / "data").rglob("RECORDS"))
if not records_files:
    raise FileNotFoundError("لم يتم العثور على ملف RECORDS داخل مجلد data.")

records_path = records_files[0]
DATA_DIR = records_path.parent

print("Using DATA_DIR:", DATA_DIR)

# 2) دالة استخراج التشخيص من voiceXXX-info.txt
def extract_diagnosis_label(info_path: Path) -> str:
    """
    يستخرج diagnosis من ملف voiceXXX-info.txt.
    يتعامل مع tab / مسافات / نقطتين.
    مثال سطر:
    Diagnosis:    hyperkinetic dysphonia
    """
    text = info_path.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        clean = line.strip()

        # بعض الملفات قد تحتوي "Diagnosis:" أو "Diagnosis\t"
        if clean.lower().startswith("diagnosis"):
            # افصل على ":" أو tab أو مسافات متكررة بعد الكلمة
            parts = re.split(r"[:\t]+", clean, maxsplit=1)
            if len(parts) == 2:
                val = parts[1].strip()
                if val:
                    return val.lower()

    return "unknown"

# 3) اختبار سريع على ملف معروف
test_info = DATA_DIR / "voice001-info.txt"
print("Example info path:", test_info)
print("Example info exists?", test_info.exists())
if test_info.exists():
    print("Parsed label from voice001-info:", extract_diagnosis_label(test_info))

# 4) اقرأ TSV
df = pd.read_csv(TSV_PATH, sep="\t")

if "record" not in df.columns:
    raise KeyError("عمود 'record' غير موجود في الداتا. لازم يكون فيه مثل voice001.")

# 5) اربط كل record بملف info الخاص به
labels = []
missing_info_files = 0

for rec in df["record"].astype(str):
    # أهم سطر: ملفات التشخيص هي voiceXXX-info.txt
    info_path = DATA_DIR / f"{rec}-info.txt"

    if info_path.exists():
        labels.append(extract_diagnosis_label(info_path))
    else:
        labels.append("unknown")
        missing_info_files += 1

df["label"] = labels

# 6) (اختياري) label_binary: 0 للـ healthy/normal و 1 لغير ذلك
healthy_words = {
    "healthy",
    "normal",
    "no pathology",
    "no-pathology",
    "none",
}
df["label_binary"] = df["label"].apply(lambda x: 0 if str(x).strip().lower() in healthy_words else 1)

# 7) احفظ فوق نفس الملف
df.to_csv(TSV_PATH, sep="\t", index=False)

print("\n✅ Added label + label_binary")
print("Saved:", TSV_PATH)
print("Missing info files:", missing_info_files, "out of", len(df))
print("Label counts (top 20):\n", df["label"].value_counts().head(20))
