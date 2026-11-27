# results

Everything the workflow makes. It can all be rebuilt with
`pixi run reproduce`, so it is not committed to Git.

| Folder | Content |
|--------|---------|
| `fastqc/` | FastQC report per read file (samples with reads) |
| `spades/<sample>/` | SPAdes assembly; `scaffolds.fasta` is used downstream |
| `quast/<sample>/` | Assembly statistics (`report.html`, `transposed_report.tsv`) |
| `prokka/<sample>/` | Genome annotation (`.gff`, `.gbk`, `.faa`, ...) |
| `abricate/<sample>/<db>.tsv` | Resistance and virulence genes found, one file per database |
| `tables/` | Summary tables read by the report and by `scripts/check_results.py` |
| `logs/` | Messages of every tool, one file per job |
