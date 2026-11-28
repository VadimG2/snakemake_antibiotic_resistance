# snakemake_antibiotic_resistance

Assembly, annotation and antimicrobial resistance (AMR) gene detection for
bacterial isolates, as a Snakemake workflow (FastQC → SPAdes → QUAST →
Prokka → Abricate) that anyone can rerun with one command.

Applied here to *Staphylococcus aureus*. Question: does the pipeline recover
the reported methicillin phenotype (MRSA or MSSA) of each isolate from its
genome, through the *mecA* gene, and which other acquired resistance genes do
the isolates carry? Data: two clinical MRSA isolates from Japan, one MSSA
isolate from Dublin, and the published MRSA reference genome USA300_FPR3757,
which enters as a ready assembly (the pipeline accepts reads or assemblies).

Author: VadimG2 (<https://github.com/VadimG2>). Capstone project of CBIO7501
*The Art of Reproducible and Open Science* (fall 2026).
Email: vadim.gvozdev@mbzuai.ac.ae

## Publication

DOI: 10.5281/zenodo.24586321 

The reference genome is described in Diep et al. (2006), *The Lancet*
367:731–739, <https://doi.org/10.1016/S0140-6736(06)68231-7>.

## Reproduce the results

Requirements: [Pixi](https://pixi.prefix.dev/latest/) (tested with 0.85) and
an internet connection. Runs on **Linux and macOS** (Intel and Apple Silicon).
Prokka and QUAST 5 have no Apple Silicon (osx-arm64) builds, so on an Apple
Silicon Mac Pixi installs the Intel (osx-64) builds of the pipeline tools and
runs them through Rosetta 2 (install it once with
`softwareupdate --install-rosetta`); expect it to be slower. The report
environment is native everywhere. On Windows use WSL2. Alternatively, use the
container image (`containers/README.md`). No other installation is needed.

```bash
git clone https://github.com/VadimG2/snakemake_antibiotic_resistance.git
cd snakemake_antibiotic_resistance
pixi install --locked            # optional: fails if pixi.lock and pixi.toml disagree
pixi run reproduce
```

`pixi run reproduce`:

1. installs the exact software versions in `pixi.lock`;
2. downloads the raw data from ENA and NCBI (`pixi run download`) and checks
   it against the providers' md5 and our sha256 (`metadata/`);
3. runs the Snakemake workflow (`pixi run run-snakemake`, 4 cores; settings in
   `config/config.yaml`);
4. compares the main results with `metadata/expected_results.tsv`
   (`pixi run check-results`);
5. renders the report `reports/amr-report.html` (`pixi run report`).

The *Reproduce* GitHub Action runs the same command from a clean clone on
every push. `pixi task list` shows every task.

## Hardware

Any recent computer with 4 cores and 8 GB of memory. Measured on 2026-11-27
on a cloud VM (2 cores of an Intel Xeon at 2.1 GHz, 7 GB of memory, Linux):
the workflow took 26 minutes, SPAdes used at most 2.4 GB of memory. Disk:
8 GB for the software environments (`.pixi/`), 222 MB for the raw data, 270 MB
for the results. Most of the time goes to SPAdes (about 8 minutes per isolate
on 2 cores).

## Outputs

| Path | Content |
|------|---------|
| `reports/amr-report.html` | The report: data, assemblies, resistance genes, software versions |
| `results/tables/amr_hits.tsv` | Every resistance and virulence gene found (all databases) |
| `results/tables/abricate_summary_<db>.tsv` | Gene presence per isolate, one file per database |
| `results/tables/assembly_stats.tsv` | QUAST statistics per assembly |
| `results/quast/`, `results/prokka/`, `results/spades/`, `results/fastqc/` | Full output of each tool |

Expected main result (NCBI AMRFinder database, 80 % identity and coverage):
*mecA* present in MRSA_K18-4-29, MRSA_K18-4-413 and USA300_FPR3757 and
absent from MSSA_Dublin, so genotype and reported phenotype agree for all four
genomes. The full list of expected genes per isolate is in
`metadata/expected_results.tsv`; `pixi run check-results` compares a new run
with it (gene lists must match exactly, assembly length within 2 %).

## Data

| Sample | Data | Source |
|--------|------|--------|
| MRSA_K18-4-29 | ENA run DRR236068 (Illumina MiSeq, paired) | BioProject PRJDB10125 |
| MRSA_K18-4-413 | ENA run DRR236029 (Illumina MiSeq, paired) | BioProject PRJDB10125 |
| MSSA_Dublin | ENA run SRR20394268 (Illumina MiSeq, paired) | BioProject PRJNA818983 |
| USA300_FPR3757 | NCBI assembly GCF_000013465.1 | BioProject PRJNA16313 |

Download links, provider checksums and our checksums are in `metadata/`; the
data is not stored in this repository. Sample information is in
`metadata/samples.tsv`.

**Data availability.** All data are publicly available from the
International Nucleotide Sequence Database Collaboration (ENA, NCBI, DDBJ)
under the accessions above. INSDC places no restrictions on their use or
redistribution; please cite the original submitters. All results can be
regenerated from them with `pixi run reproduce`.

## Repository contents

See `docs/structure.md` (each folder also has its own README). Analysis
decisions, with reasons, are in `docs/decisions.md`.

## Cite

Archived on Zenodo (sandbox, for the course): 
**DOI** 10.5281/zenodo.24586320, (all versions). 

See`CITATION.cff` (GitHub: "Cite this repository"). Please also cite the
tools: SPAdes, QUAST, Prokka, Abricate and its databases (listed in the
report).

## License

Code: MIT (`LICENSE`). Report text and figures: CC BY 4.0
(`LICENSE-CC-BY-4.0.txt`). Data: INSDC, no restrictions (see Data).
`scripts/download_data.py`, `containers/Dockerfile` and
`.github/workflows/reproduce.yml` are adapted from the CBIO7501 course
materials (MIT).

## Contact

Questions and problems: open an issue on GitHub. Contributions: see
`CONTRIBUTING.md`. Everyone taking part follows `CODE_OF_CONDUCT.md`.
