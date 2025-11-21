import pandas as pd
import sys

inp = sys.argv[1]
outp = sys.argv[2]

df = pd.read_csv(inp)

# Placeholder: add basic flag, not real geocoding
if "latitude" not in df.columns:
    df["latitude"] = None
if "longitude" not in df.columns:
    df["longitude"] = None

df["geocode_status"] = df.apply(
    lambda row: "missing" if pd.isna(row["latitude"]) else "ok",
    axis=1
)

df.to_csv(outp, index=False)
