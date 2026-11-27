"""Collect the per-sample outputs of the workflow into four tables.

Called by the `summarise` rule of workflow/Snakefile; the report and
scripts/check_results.py read the tables it writes:

  assembly_stats.tsv    QUAST metrics, one row per sample
  read_stats.tsv        read counts, length and GC from FastQC, one row per file
  annotation_stats.tsv  Prokka feature counts, one row per sample
  amr_hits.tsv          every Abricate hit of every database, with the sample

Only the Python standard library is used.
"""

import argparse
import csv
import io
import zipfile
from pathlib import Path

QUAST_COLUMNS = {
    "# contigs": "contigs",
    "Largest contig": "largest_contig",
    "Total length": "total_length",
    "GC (%)": "gc_percent",
    "N50": "n50",
    "L50": "l50",
    "# N's per 100 kbp": "n_per_100kbp",
}


def write_tsv(path, rows, fields):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_samples(path):
    with open(path) as fh:
        return {row["sample"]: row for row in csv.DictReader(fh, delimiter="\t")}


def assembly_stats(paths, samples):
    rows = []
    for path in paths:
        sample = Path(path).parent.name
        with open(path) as fh:
            record = next(csv.DictReader(fh, delimiter="\t"))
        row = {"sample": sample, "source": "provided" if samples[sample]["assembly"] else "SPAdes"}
        row.update({new: record[old] for old, new in QUAST_COLUMNS.items()})
        rows.append(row)
    return rows, ["sample", "source", *QUAST_COLUMNS.values()]


def read_stats(paths):
    rows = []
    for path in paths:
        sample, read = Path(path).name.removesuffix("_fastqc.zip").rsplit("_R", 1)
        with zipfile.ZipFile(path) as zf:
            name = next(n for n in zf.namelist() if n.endswith("fastqc_data.txt"))
            text = io.TextIOWrapper(zf.open(name), encoding="utf-8").read()
        values = dict(line.split("\t", 1) for line in text.splitlines() if "\t" in line and not line.startswith(("#", ">>")))
        rows.append({
            "sample": sample,
            "read": read,
            "sequences": values["Total Sequences"],
            "length": values["Sequence length"],
            "gc_percent": values["%GC"],
        })
    return rows, ["sample", "read", "sequences", "length", "gc_percent"]


def annotation_stats(paths):
    rows, fields = [], ["sample"]
    for path in paths:
        row = {"sample": Path(path).parent.name}
        for line in Path(path).read_text().splitlines():
            key, _, value = line.partition(":")
            if key != "organism" and value.strip():
                row[key.strip()] = value.strip()
                if key.strip() not in fields:
                    fields.append(key.strip())
        rows.append(row)
    return rows, fields


def amr_hits(paths):
    rows = []
    fields = ["sample", "database", "gene", "contig", "start", "end", "coverage_percent",
              "identity_percent", "accession", "product", "resistance"]
    for path in paths:
        sample = Path(path).parent.name
        with open(path) as fh:
            for record in csv.DictReader(fh, delimiter="\t"):
                rows.append({
                    "sample": sample,
                    "database": record["DATABASE"],
                    "gene": record["GENE"],
                    "contig": record["SEQUENCE"],
                    "start": record["START"],
                    "end": record["END"],
                    "coverage_percent": record["%COVERAGE"],
                    "identity_percent": record["%IDENTITY"],
                    "accession": record["ACCESSION"],
                    "product": record["PRODUCT"],
                    "resistance": record["RESISTANCE"],
                })
    rows.sort(key=lambda r: (r["sample"], r["database"], r["gene"], r["contig"], int(r["start"])))
    return rows, fields


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--samples", required=True)
    parser.add_argument("--quast", nargs="+", required=True)
    parser.add_argument("--prokka", nargs="+", required=True)
    parser.add_argument("--fastqc", nargs="*", default=[])
    parser.add_argument("--abricate", nargs="+", required=True)
    parser.add_argument("--out-assembly", required=True)
    parser.add_argument("--out-reads", required=True)
    parser.add_argument("--out-annotation", required=True)
    parser.add_argument("--out-amr", required=True)
    args = parser.parse_args()

    samples = read_samples(args.samples)
    write_tsv(args.out_assembly, *assembly_stats(args.quast, samples))
    write_tsv(args.out_reads, *read_stats(args.fastqc))
    write_tsv(args.out_annotation, *annotation_stats(args.prokka))
    write_tsv(args.out_amr, *amr_hits(args.abricate))


if __name__ == "__main__":
    main()
