#!/usr/bin/env python3
"""Build inst/extdata/colonial/*.parquet from the transcribed CSVs.

Reads <table>.csv from data-raw/colonial_census/csv/ (1906 and 1931 census
volumes) or data-raw/yearbook_demography/csv/ (Statistique generale de la
Tunisie yearbooks), and the table index data-raw/colonial_census/tables.csv
(table, census, table_id, title_fr, title_en, pages, value_type). In the
index, census is "eur1906", "ind1931" or "sgt"; rows of an "sgt" table carry
the edition code (sgt1922 ... sgt1939) and their volume's gallica_ark. It writes one Zstandard-compressed Parquet file
per table plus index.parquet, which load_colonial_census() and
colonial_census_tables() read.

Usage:  pip install pandas pyarrow && python3 data-raw/colonial_census/build.py
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
CSV_DIRS = [HERE / "csv", HERE.parent / "yearbook_demography" / "csv",
            HERE.parent / "yearbook_health_education" / "csv",
            HERE.parent / "yearbook_other_chapters" / "csv"]
OUT = HERE.parent.parent / "inst" / "extdata" / "colonial"
ARKS = {"eur1906": "bd6t53563851", "ind1931": "bpt6k994559s"}
INT_COLS = {"census_year", "base_year", "duplicate", "year", "row_order"}
REQUIRED = ["census", "table_id", "source_page", "gallica_view", "value", "flag"]
FLAGS = {"", "ocr_corrected", "illegible", "total_mismatch", "derived_from_totals",
         "not_applicable", "reprint_corrected"}


def find(table):
    hits = [d / f"{table}.csv" for d in CSV_DIRS if (d / f"{table}.csv").exists()]
    if len(hits) != 1:
        raise SystemExit(f"{table}: expected one CSV, found {hits}")
    return hits[0]


def load(table):
    df = pd.read_csv(find(table), dtype=str, keep_default_na=False, encoding="utf-8-sig")
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise SystemExit(f"{table}: missing columns {missing}")
    bad = set(df["flag"]) - FLAGS
    if bad:
        raise SystemExit(f"{table}: unknown flags {bad}")
    for c in ("source_page", "gallica_view"):
        df[c] = pd.to_numeric(df[c], errors="raise").astype("int32")
    for c in INT_COLS & set(df.columns):
        df[c] = pd.to_numeric(df[c].replace("", None), errors="raise").astype("Int32")
    df["value"] = pd.to_numeric(df["value"].replace("", None), errors="raise")
    if (df["value"].dropna() % 1 == 0).all():
        df["value"] = df["value"].astype("Int64")
    # empty strings → NA in text columns, so R sees NA_character_
    for c in df.columns:
        if pd.api.types.is_string_dtype(df[c]) and not pd.api.types.is_numeric_dtype(df[c]):
            df[c] = df[c].astype(object).where(df[c] != "", None)
    return df


def write(df, path):
    """Write Parquet with plain (not large_) string columns, for portability."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    tbl = pa.Table.from_pandas(df, preserve_index=False)
    # plain strings, and all-empty columns (Arrow type null) as strings too,
    # so R reads them as character rather than an unspecified logical
    schema = pa.schema([pa.field(f.name, pa.string())
                        if pa.types.is_large_string(f.type) or pa.types.is_null(f.type) else f
                        for f in tbl.schema]).remove_metadata()
    pq.write_table(tbl.cast(schema), path, compression="zstd")


def main():
    idx = pd.read_csv(HERE / "tables.csv", dtype=str, keep_default_na=False)
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for _, r in idx.iterrows():
        df = load(r["table"])
        if r["census"] == "sgt":
            if not df["census"].str.startswith("sgt").all() or "gallica_ark" not in df.columns:
                raise SystemExit(f"{r['table']}: yearbook rows need sgt* census codes and gallica_ark")
            ark = ";".join(sorted(df["gallica_ark"].dropna().unique()))
        else:
            if not (df["census"] == r["census"]).all():
                raise SystemExit(f"{r['table']}: census column does not match the index")
            ark = ARKS[r["census"]]
        write(df, OUT / f"{r['table']}.parquet")
        rows.append({**r.to_dict(), "gallica_ark": ark, "n_rows": len(df)})
        print(f"{r['table']}: {len(df)} rows, {df.shape[1]} columns")
    stale = {p.stem for p in OUT.glob("*.parquet")} - set(idx["table"]) - {"index"}
    for s in stale:
        (OUT / f"{s}.parquet").unlink()
        print(f"removed stale {s}.parquet")
    out = pd.DataFrame(rows)[["table", "census", "table_id", "title_fr", "title_en", "pages",
                              "gallica_ark", "n_rows", "value_type"]]
    out["n_rows"] = out["n_rows"].astype("int32")
    write(out, OUT / "index.parquet")
    print(f"index: {len(out)} tables")


if __name__ == "__main__":
    main()
