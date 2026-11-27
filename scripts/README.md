# scripts

| Script | What it does | Run by |
|--------|--------------|--------|
| `download_data.py` | Downloads the raw data, checks provider md5 and our sha256, makes it read-only | `pixi run download` |
| `summarise.py` | Collects QUAST, FastQC, Prokka and Abricate outputs into `results/tables/` | the `summarise` rule |
| `check_results.py` | Compares the main results with `metadata/expected_results.tsv` | `pixi run check-results` |

Run scripts from the project folder; all paths are relative to it.
