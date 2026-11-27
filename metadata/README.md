# metadata

Files that describe the raw data. They are small, written by hand (or by a
script named below) and committed.

## sources.tsv

Where each raw file comes from. Columns: `name`; `url` (download link);
`md5` (checksum published by the provider: the ENA file report `fastq_md5`
for reads, NCBI's `md5checksums.txt` for the assembly; copied 2026-11-27);
`unpack` (`none` = keep the file as is); `dest` (where it goes in the project).

## checksums.sha256

SHA-256 checksum of every raw file we keep. Checked by
`scripts/download_data.py`; by hand: `sha256sum -c metadata/checksums.sha256`.

## samples.tsv

One row per isolate (the sample sheet of the workflow).

| Column | Meaning |
|--------|---------|
| sample | Name used in all result files |
| strain | Strain name given by the submitters |
| phenotype | Methicillin phenotype reported by the submitters (`MRSA` or `MSSA`) |
| country | Country of isolation |
| study | ENA/NCBI BioProject |
| biosample | BioSample accession |
| run_or_assembly | ENA run accession, or NCBI assembly accession |
| fastq_1, fastq_2 | Read files, relative to the project folder (empty for an assembly) |
| assembly | Assembly file (empty for samples with reads) |

Phenotypes come from the BioSample titles: "Clinical isolate of Methicillin
resistant *Staphylococcus aureus*" (PRJDB10125), "WGS of MSSA recovered in
Dublin hospital" (PRJNA818983). USA300_FPR3757 is the published MRSA
reference genome (Diep et al. 2006).

