"""Compare the main results with the values recorded in metadata/expected_results.tsv.

The main result of the project is the set of resistance genes found in each
isolate, and whether mecA (methicillin resistance) is present. Gene sets must
match exactly; assembly length may differ by the tolerance in the table
(SPAdes can give slightly different assemblies on other machines).

Usage:  pixi run check-results          (after the workflow)
        python scripts/check_results.py --write   (record the current results)
Exit code 1 if any check fails.
"""

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPECTED = ROOT / "metadata" / "expected_results.tsv"
TABLES = ROOT / "results" / "tables"
LENGTH_TOLERANCE = 0.02  # relative


def read_tsv(path):
    with open(path) as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def observed():
    genes = defaultdict(set)
    for hit in read_tsv(TABLES / "amr_hits.tsv"):
        genes[(hit["sample"], hit["database"])].add(hit["gene"])
    values = {}
    for row in read_tsv(TABLES / "assembly_stats.tsv"):
        sample = row["sample"]
        values[(sample, "total_length")] = row["total_length"]
        values[(sample, "mecA")] = "yes" if "mecA" in genes[(sample, "ncbi")] else "no"
        values[(sample, "resfinder_genes")] = ";".join(sorted(genes[(sample, "resfinder")])) or "none"
        values[(sample, "ncbi_genes")] = ";".join(sorted(genes[(sample, "ncbi")])) or "none"
    return values


def matches(check, expected, got):
    if check == "total_length":
        return abs(int(got) - int(expected)) <= LENGTH_TOLERANCE * int(expected)
    return got == expected


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--write", action="store_true", help="write the current results as the expected ones")
    args = parser.parse_args()

    values = observed()
    if args.write:
        with open(EXPECTED, "w", newline="") as fh:
            writer = csv.writer(fh, delimiter="\t", lineterminator="\n")
            writer.writerow(["sample", "check", "expected"])
            for (sample, check), value in sorted(values.items()):
                writer.writerow([sample, check, value])
        print(f"Wrote {len(values)} expected values to {EXPECTED.relative_to(ROOT)}")
        return

    failed = 0
    for row in read_tsv(EXPECTED):
        got = values.get((row["sample"], row["check"]), "missing")
        ok = got != "missing" and matches(row["check"], row["expected"], got)
        failed += not ok
        status = "OK  " if ok else "DIFF"
        detail = "" if ok else f"  (expected {row['expected']}, got {got})"
        print(f"{status} {row['sample']:<16} {row['check']:<16} {got}{detail}")
    if failed:
        sys.exit(f"{failed} check(s) differ from {EXPECTED.relative_to(ROOT)}")
    print("All results match the expected values.")


if __name__ == "__main__":
    main()
