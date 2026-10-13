"""Kiểm tra IMDb và chia train/validation/test trước khi học đặc trưng."""
from pathlib import Path
import html
import json
import re

import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent


def normalize_text(text):
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def load_dataset(path):
    data = pd.read_csv(path)
    if not {"review", "sentiment"}.issubset(data.columns):
        raise ValueError("Dataset cần có hai cột review và sentiment.")
    data.insert(0, "source_id", range(len(data)))
    return data


def inspect_dataset(data):
    text = data["review"].fillna("").astype(str)
    label = data["sentiment"].astype("string").str.strip().str.lower()
    normalized = text.map(normalize_text)
    valid = normalized.ne("") & label.notna() & label.ne("").fillna(False)
    valid_data = pd.DataFrame({"text": normalized[valid], "label": label[valid]})
    conflicts = valid_data.groupby("text")["label"].nunique()
    lengths = normalized.str.split().str.len()
    return {
        "samples": len(data),
        "classes": int(label.nunique()),
        "class_counts": label.value_counts().to_dict(),
        "missing_text": int(data["review"].isna().sum()),
        "empty_text_after_normalization": int(normalized.eq("").sum()),
        "missing_labels": int(label.isna().sum()),
        "empty_labels": int(label.eq("").sum()),
        "exact_duplicate_reviews": int(text.duplicated().sum()),
        "normalized_duplicate_reviews": int(normalized.duplicated().sum()),
        "conflicting_texts": int(conflicts.gt(1).sum()),
        "document_length_words": lengths.describe(percentiles=[0.5, 0.9, 0.95]).to_dict(),
    }


def clean_dataset(data):
    data = data.copy()
    data["text"] = data["review"].fillna("").astype(str).map(normalize_text)
    data["label"] = data["sentiment"].astype("string").str.strip().str.lower()
    valid = data["text"].ne("") & data["label"].notna() & data["label"].ne("").fillna(False)
    data = data.loc[valid].copy()
    if not data["label"].isin(["positive", "negative"]).all():
        raise ValueError("Phát hiện nhãn ngoài positive/negative.")
    # Không tự chọn nhãn khi cùng một nội dung có nhiều nhãn khác nhau.
    label_counts = data.groupby("text")["label"].transform("nunique")
    data = data.loc[label_counts.eq(1)].drop_duplicates("text", keep="first")
    return data[["source_id", "review", "text", "label"]].reset_index(drop=True)


def split_dataset(data, random_state=42):
    train, remaining = train_test_split(
        data, test_size=0.4, stratify=data["label"], random_state=random_state
    )
    validation, test = train_test_split(
        remaining, test_size=0.5, stratify=remaining["label"], random_state=random_state
    )
    splits = {"train": train, "validation": validation, "test": test}
    names = list(splits)
    for index, name in enumerate(names):
        for other in names[index + 1:]:
            assert set(splits[name]["text"]).isdisjoint(splits[other]["text"])
            assert set(splits[name]["source_id"]).isdisjoint(splits[other]["source_id"])
    assert sum(len(part) for part in splits.values()) == len(data)
    return {name: part.reset_index(drop=True) for name, part in splits.items()}


def summarize_splits(splits):
    total = sum(len(part) for part in splits.values())
    rows = []
    for name, part in splits.items():
        counts = part["label"].value_counts()
        rows.append({
            "split": name,
            "samples": len(part),
            "percentage": 100 * len(part) / total,
            "negative": int(counts.get("negative", 0)),
            "positive": int(counts.get("positive", 0)),
        })
    return pd.DataFrame(rows)


def prepare_dataset(path=ROOT / "imdb.zip", output_dir=ROOT / "data"):
    raw = load_dataset(path)
    report = inspect_dataset(raw)
    cleaned = clean_dataset(raw)
    splits = split_dataset(cleaned)
    summary = summarize_splits(splits)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, part in splits.items():
        part.to_csv(output_dir / f"{name}.csv", index=False)
    summary.to_csv(output_dir / "split_summary.csv", index=False)
    report.update({"clean_samples": len(cleaned), "removed_rows": len(raw) - len(cleaned),
                   "random_state": 42, "split_ratios": [0.6, 0.2, 0.2]})
    (output_dir / "inspection.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return raw, cleaned, splits, summary, report


if __name__ == "__main__":
    _, _, _, summary, report = prepare_dataset()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(summary.to_string(index=False))
