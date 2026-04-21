import pandas as pd

# Load metadata
meta = pd.read_csv("metadata.csv")

# Standardize severity column (fix capitalization inconsistency)
meta["how_severe_is_your_stuttering"] = meta["how_severe_is_your_stuttering"].str.lower().str.strip()
meta["do_you_stutter_while_speaking"] = meta["do_you_stutter_while_speaking"].str.lower().str.strip()

# Rename uId to speaker_id for merging
meta = meta.rename(columns={"uId": "speaker_id"})

print(meta.head())
print(meta["how_severe_is_your_stuttering"].value_counts())
print(meta["do_you_stutter_while_speaking"].value_counts())

# Load your transcript CSV
df = pd.read_csv("disfluency_data.csv")

# Make sure speaker_id is same type in both
df["speaker_id"] = df["speaker_id"].astype(int)
meta["speaker_id"] = meta["speaker_id"].astype(int)

# Merge
merged = df.merge(meta, on="speaker_id", how="left")

print(merged.head())
print(f"\nTotal matched records: {merged['age'].notna().sum()}")

# Save merged file
merged.to_csv("merged_analysis.csv", index=False)