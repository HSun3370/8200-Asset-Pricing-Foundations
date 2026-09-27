"""
Pset 1, Question 3(a) -- step 1: apply the industry exclusions to CRSP.csv IN PLACE.

Student specification:
  Drop rows with 4900 <= SIC <= 4949 (utilities) or 6000 <= SIC <= 6999 (financials),
  deleting those rows directly in CRSP.csv.
  Rows whose SICCD does not parse as a number are KEPT (student's decision) -- they are
  not demonstrably utilities or financials.

The WRDS extract already restricts to SHRCD in {10, 11}, EXCHCD in {1, 2, 3}, and
1963-06 onward, so no further screens are applied here.

This rewrites CRSP.csv. It is idempotent: re-running it on an already-filtered file
detects that there is nothing to drop and leaves the file alone. Every column is read
and written as text so the surviving rows are byte-identical to the original.

Run this once, before q3a.py.
"""

import os
from pathlib import Path

import pandas as pd

PSET_DIR = Path(__file__).resolve().parents[1]
CRSP_CSV = PSET_DIR / "CRSP.csv"

UTILITIES = (4900, 4949)
FINANCIALS = (6000, 6999)


def main() -> None:
    df = pd.read_csv(CRSP_CSV, dtype=str)
    n_before = len(df)

    sic = pd.to_numeric(df["SICCD"], errors="coerce")
    drop = sic.between(*UTILITIES) | sic.between(*FINANCIALS)

    n_util = int(sic.between(*UTILITIES).sum())
    n_fin = int(sic.between(*FINANCIALS).sum())
    n_unparsed = int(sic.isna().sum())

    print(f"rows before            : {n_before:,}")
    print(f"  utilities  4900-4949 : {n_util:,}")
    print(f"  financials 6000-6999 : {n_fin:,}")
    print(f"  SICCD unparseable    : {n_unparsed:,}  (kept)")

    if not drop.any():
        print("\nnothing to drop - CRSP.csv is already filtered, leaving it unchanged.")
        return

    kept = df.loc[~drop]
    # Write to a sibling temp file first, then atomically replace, so an interrupted
    # run cannot leave CRSP.csv truncated.
    tmp = CRSP_CSV.with_suffix(".csv.tmp")
    kept.to_csv(tmp, index=False)
    os.replace(tmp, CRSP_CSV)

    print(f"rows after             : {len(kept):,}  (dropped {n_before - len(kept):,})")
    print(f"rewrote {CRSP_CSV}")


if __name__ == "__main__":
    main()
