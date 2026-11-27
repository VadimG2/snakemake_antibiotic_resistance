# Decision log

- 2025: first version of the pipeline (FastQC, SPAdes, QUAST, Prokka,
  Abricate), tested on three SARS-CoV-2 runs (SRR31122807–09) with
  per-rule Conda environments.
- 2026-11-27: the test runs were SARS-CoV-2, a virus, so an antimicrobial
  resistance (AMR) screen could only find nothing. Replaced them with
  *Staphylococcus aureus*: a small genome (2.8 Mb, fast to assemble on a
  CI runner) and a clear genotype-phenotype question (mecA and methicillin
  resistance). Two MRSA (PRJDB10125), one MSSA (PRJNA818983) and the MRSA
  reference genome USA300_FPR3757 as a provided assembly (positive control
  for the assembly-input mode).
- 2026-11-27: folder layout from the course Cookiecutter template
  (`cookiecutter-repro-project`). Cookiecutter only creates new folders, so
  the template was generated in a temporary folder and its folders, READMEs,
  `.gitignore` and `.gitattributes` were copied into this repository; its
  `README.md`, `pixi.toml`, `CITATION.cff`, `LICENSE` and CI workflow were
  replaced by project-specific ones in later pull requests.
- 2026-11-27: raw data no longer in Git; downloaded from ENA and NCBI by
  `scripts/download_data.py`, checked against provider md5 and our sha256.
- 2026-11-27: software from one Pixi environment (`pipeline`, locked in
  `pixi.lock`) instead of unpinned per-rule `conda:` files. `envs/pipeline.yml` is
  exported from `pixi.toml` (`pixi workspace export conda-environment`) for
  people without Pixi, not written by hand. Snakemake is
  launched through Pixi, so every rule runs with locked versions
  (`snakemake --lint` still suggests per-rule environments; see CBIO7501
  lesson 09). All tools solve together on linux-64 and osx-64; Prokka has no
  osx-arm64 build, so osx-arm64 is not listed for the pipeline: on Apple
  Silicon, Pixi installs the osx-64 packages and runs them with Rosetta 2
  (Pixi's documented fallback). Not yet tested on an Apple Silicon Mac.
- 2026-11-27: QUAST 5.3 imports `distutils`, removed in Python 3.12;
  `setuptools <81` in the environment provides it.
- 2026-11-27: SPAdes in `--isolate` mode (recommended for high-coverage
  isolates, faster). Prokka with `--compliant`, because SPAdes contig
  names can exceed Prokka's 37-character limit.
- 2026-11-27: Abricate thresholds 80 % identity and 80 % coverage, and four
  bundled databases: ResFinder and NCBI AMRFinder (resistance), CARD
  (resistance, broader), VFDB (virulence). mecA is called from NCBI AMRFinder.
- 2026-11-27: settings moved from `params.json` (partly ignored by the old
  Snakefile) to `config/config.yaml`; results go to `results/`.
