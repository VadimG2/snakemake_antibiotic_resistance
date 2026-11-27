# Project structure

Created from the CBIO7501 Cookiecutter template
(`templates/cookiecutter-repro-project` in
<https://github.com/khan-lab/cbio7501-f26>), which follows Noble (2009) and
Wilson et al. (2017).

| Folder | What goes in it | Rule |
|--------|-----------------|------|
| `data/raw/` | Reads (ENA) and assembly (NCBI), downloaded by `scripts/download_data.py` | Read-only, not committed |
| `data/processed/` | Data derived from raw data (decompressed assembly) | Rebuilt by the workflow |
| `metadata/` | Sample sheet, data sources, checksums, expected results | Committed |
| `config/` | Workflow settings (`config.yaml`) | Committed |
| `workflow/` | `Snakefile` | Committed |
| `scripts/` | Download, summary and checking code | Committed |
| `reports/` | Quarto report source and bibliography | Source committed, HTML not |
| `results/` | Everything the workflow produces | Rebuilt, not committed |
| `notebooks/` | Jupyter notebooks for exploration (none yet) | Committed |
| `envs/` | `pipeline.yml`: Conda environment exported from `pixi.toml`, for people without Pixi | Generated, committed |
| `docs/` | This file, the decision log | Committed |
| `containers/` | `Dockerfile`, built from `pixi.lock` | Committed |
| `.github/workflows/` | Reproduce-from-a-clean-clone check, container build | Committed |
