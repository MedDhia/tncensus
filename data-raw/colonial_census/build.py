#!/usr/bin/env python3
"""Build inst/extdata/colonial/*.parquet from the transcribed CSVs.

Reads data-raw/colonial_census/csv/<table>.csv and the table index
data-raw/colonial_census/tables.csv (table, census, table_id, title_fr,
title_en, pages, value_type). It writes one Zstandard-compressed Parquet file
per table plus index.parquet, which load_colonial_census() and
colonial_census_tables() read.

Usage:  pip install pandas pyarrow && python3 data-raw/colonial_census/build.py
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE.parent.parent / "inst" / "extdata" / "colonial"
ARKS = {"eur1906": "bd6t53563851", "ind1931": "bpt6k994559s"}
REQUIRED = ["census", "table_id", "source_page", "gallica_view", "value", "flag"]
FLAGS = {"", "ocr_corrected", "illegible", "total_mismatch"}


def load(table):
    df = pd.read_csv(HERE / "csv" / f"{table}.csv", dtype=str, keep_default_na=False,
                     encoding="utf-8-sig")
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise SystemExit(f"{table}: missing columns {missing}")
    bad = set(df["flag"]) - FLAGS
    if bad:
        raise SystemExit(f"{table}: unknown flags {bad}")
    for c in ("source_page", "gallica_view"):
        df[c] = pd.to_numeric(df[c], errors="raise").astype("int32")
    df["value"] = pd.to_numeric(df["value"].replace("", None), errors="raise")
    if (df["value"].dropna() % 1 == 0).all():
        df["value"] = df["value"].astype("Int64")
    # empty strings → NA in text columns, so R sees NA_character_
    for c in df.columns:
        if df[c].dtype == object:
            df[c] = df[c].replace("", None)
    return df


def main():
    idx = pd.read_csv(HERE / "tables.csv", dtype=str, keep_default_na=False)
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for _, r in idx.iterrows():
        df = load(r["table"])
        df.to_parquet(OUT / f"{r['table']}.parquet", compression="zstd", index=False)
        rows.append({**r.to_dict(), "gallica_ark": ARKS[r["census"]], "n_rows": len(df)})
        print(f"{r['table']}: {len(df)} rows, {df.shape[1]} columns")
    stale = {p.stem for p in OUT.glob("*.parquet")} - set(idx["table"]) - {"index"}
    for s in stale:
        (OUT / f"{s}.parquet").unlink()
        print(f"removed stale {s}.parquet")
    out = pd.DataFrame(rows)[["table", "census", "table_id", "title_fr", "title_en", "pages",
                              "gallica_ark", "n_rows", "value_type"]]
    out["n_rows"] = out["n_rows"].astype("int32")
    out.to_parquet(OUT / "index.parquet", compression="zstd", index=False)
    print(f"index: {len(out)} tables")


if __name__ == "__main__":
    main()
