"""
Add the PRC and SHROUT columns to CRSP.csv IN PLACE.

Student specification:
  Merge Pset 1/n7kuxmiirhelss1l.csv into Pset 1/CRSP.csv on (PERMNO, date), keyed on
  CRSP.csv -- i.e. a left join that keeps exactly the rows already in CRSP.csv and
  appends the PRC and SHROUT columns.

The source file is the same WRDS extract as CRSP.csv but unfiltered (3,435,060 rows vs
2,734,812 after the SIC exclusions in q3a_filter_crsp.py) and carries PRC/SHROUT in
place of PERMCO/RET. Both sides are unique on (PERMNO, date) and every CRSP.csv key is
present in the source, so the join adds columns without adding or dropping any row.

PRC and SHROUT are copied across verbatim. In particular PRC keeps CRSP's sign
convention -- a negative value is a bid/ask midpoint rather than a closing trade price
(500,022 rows) -- and blanks stay blank (32,726 PRC, 2,455 SHROUT). Taking the absolute
value, and deciding how to treat missing or zero entries, belongs to the market-equity
construction in Q3(b), not to this merge.

Every column is read and written as text so the existing columns stay byte-identical.
The result is written to a temp file and atomically swapped in, and the script is
idempotent: if PRC/SHROUT are already present it leaves CRSP.csv alone.
"""

import os
from pathlib import Path

import pandas as pd

PSET_DIR = Path(__file__).resolve().parents[1]
CRSP_CSV = PSET_DIR / "CRSP.csv"
SOURCE_CSV = PSET_DIR / "n7kuxmiirhelss1l.csv"

KEYS = ["PERMNO", "date"]
ADD = ["PRC", "SHROUT"]


def main() -> None:
    crsp = pd.read_csv(CRSP_CSV, dtype=str)
    print(f"CRSP.csv rows            : {len(crsp):,}")
    print(f"CRSP.csv columns         : {list(crsp.columns)}")

    already = [c for c in ADD if c in crsp.columns]
    if already:
        print(f"\n{', '.join(already)} already present - leaving CRSP.csv unchanged.")
        return

    if not SOURCE_CSV.exists():
        raise SystemExit(f"source file not found: {SOURCE_CSV}")

    src = pd.read_csv(SOURCE_CSV, dtype=str, usecols=KEYS + ADD)
    print(f"source rows              : {len(src):,}")

    dup = int(src.duplicated(subset=KEYS).sum())
    if dup:
        raise SystemExit(f"source has {dup:,} duplicate (PERMNO, date) keys; merge would "
                         "add rows. Resolve before continuing.")

    n_before = len(crsp)
    merged = crsp.merge(src, on=KEYS, how="left", indicator=True)

    unmatched = int((merged["_merge"] == "left_only").sum())
    print(f"unmatched CRSP rows      : {unmatched:,}")
    if len(merged) != n_before:
        raise SystemExit(f"row count changed ({n_before:,} -> {len(merged):,}); aborting.")
    merged = merged.drop(columns="_merge")

    tmp = CRSP_CSV.with_suffix(".csv.tmp")
    merged.to_csv(tmp, index=False)
    os.replace(tmp, CRSP_CSV)

    print(f"\nrows after               : {len(merged):,}  (unchanged)")
    print(f"columns after            : {list(merged.columns)}")
    print(f"rewrote {CRSP_CSV}")


if __name__ == "__main__":
    main()
