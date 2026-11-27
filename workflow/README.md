# workflow

`Snakefile`: the Snakemake workflow (FastQC, SPAdes, QUAST, Prokka, Abricate
and the summary tables). Settings come from `config/config.yaml`, samples
from `metadata/samples.tsv`. Run it through Pixi so every tool comes from
`pixi.lock`: `pixi run run-snakemake`, or
`pixi run -e pipeline snakemake --cores 4`.
