"""
Pset 1, Question 3(a) -- fallback builder for the Chen-Zimmermann signal cache.

`openassetpricing` serves everything from a Google Drive share that intermittently
returns "Quota exceeded" instead of data, which blocks `openap.dl_signal(...)` (and the
OpenAP constructor, which reads SignalDoc.csv). There is no non-Drive mirror.

Workaround: download the three per-signal CSVs by hand from a browser while signed in to
a Google account (if Drive shows the quota page, use "Add shortcut to Drive" / "Make a
copy" and download your own copy, which has a fresh quota), then run this script.

  Mom12m.csv  https://drive.google.com/file/d/1K2IDDXDQjKN9XHj3H4LvnjevOS3SIsgc/view
  BMdec.csv   https://drive.google.com/file/d/1dMzq7NdQcFLI7xJ-5s2aKuh56dGllyOZ/view
  GP.csv      https://drive.google.com/file/d/1ma_K3bvc_sY7RVZnTgtXJSW0tAxrYcHS/view

Put them in Pset 1/data_cache/raw/ keeping those file names, then:

  .venv\\Scripts\\python.exe "Pset 1/code/q3a_build_cz_cache.py"

This reproduces exactly what `openap.dl_signal('pandas', ['BMdec','Mom12m','GP'])`
returns with signed=False (an outer join on permno/yyyymm, rows where all three signals
are null dropped, signals cast to float, sorted) and writes data_cache/cz_signals.parquet,
which q3a.py reads. It makes no empirical choices.
"""

from pathlib import Path

import polars as pl

PSET_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = PSET_DIR / "data_cache" / "raw"
CACHE = PSET_DIR / "data_cache" / "cz_signals.parquet"

SIGNALS = ["BMdec", "Mom12m", "GP"]


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    missing = [s for s in SIGNALS if not (RAW_DIR / f"{s}.csv").exists()]
    if missing:
        raise SystemExit(
            f"missing {', '.join(f'{s}.csv' for s in missing)} in {RAW_DIR}\n"
            "See the module docstring for the download links."
        )

    df = pl.DataFrame(schema={"permno": pl.Int32, "yyyymm": pl.Int32})
    for s in SIGNALS:
        t = pl.read_csv(RAW_DIR / f"{s}.csv").with_columns(
            pl.col("permno", "yyyymm").cast(pl.Int32)
        )
        print(f"{s:8s} rows={len(t):,}")
        df = df.join(t, how="full", on=["permno", "yyyymm"], coalesce=True)

    df = (
        df.select("permno", "yyyymm", pl.col(SIGNALS))
        .filter(pl.any_horizontal(pl.col(SIGNALS)).is_not_null())
        .with_columns(pl.exclude("permno", "yyyymm").cast(pl.Float64))
        .sort("permno", "yyyymm")
    )

    df.to_pandas().to_parquet(CACHE, index=False)
    print(f"\ncombined rows: {len(df):,}")
    print(f"wrote {CACHE}")


if __name__ == "__main__":
    main()
