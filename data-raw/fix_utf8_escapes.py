#!/usr/bin/env python3
"""Decode literal UTF-8 byte escapes in the package's Parquet files.

Some text cells stored their UTF-8 bytes as escape text: "Béja" was stored as
the 11-character string "B<c3><a9>ja", and every Arabic name as a run of
escapes such as "<d9><82><d8><b1>...". This rewrites each run of "<xx>" escapes
as the bytes it spells and decodes them as UTF-8. Cells without escapes are
untouched; files without any are not rewritten. Schema and Zstandard
compression are kept.

Run once from the repository root:  python3 data-raw/fix_utf8_escapes.py
The R datasets in data/ are fixed by data-raw/fix_utf8_escapes.R.
"""
import re
import sys
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent.parent
RUN = re.compile(r"(?:<[0-9a-f]{2}>)+")
HEX = re.compile(r"<([0-9a-f]{2})>")


def decode(s):
    if s is None or "<" not in s:
        return s
    return RUN.sub(lambda m: bytes(int(h, 16) for h in HEX.findall(m.group(0))).decode("utf-8"), s)


def main():
    total = 0
    for path in sorted((ROOT / "inst" / "extdata").rglob("*.parquet")):
        tbl = pq.read_table(path)
        cols, changed = [], 0
        for name in tbl.column_names:
            col = tbl.column(name)
            if pa.types.is_string(col.type) or pa.types.is_large_string(col.type):
                vals = col.to_pylist()
                new = [decode(v) for v in vals]
                n = sum(a != b for a, b in zip(vals, new))
                if n:
                    changed += n
                    col = pa.chunked_array([pa.array(new, type=col.type)])
            cols.append(col)
        if not changed:
            continue
        out = pa.Table.from_arrays(cols, schema=tbl.schema)
        assert out.num_rows == tbl.num_rows and out.schema.equals(tbl.schema)
        pq.write_table(out, path, compression="zstd")
        total += changed
        print(f"{path.relative_to(ROOT)}: {changed} cells decoded")
    print(f"total: {total} cells", file=sys.stderr)


if __name__ == "__main__":
    main()
