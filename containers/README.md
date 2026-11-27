# containers

`Dockerfile`: builds an image of the `pipeline` environment from `pixi.lock`,
so the container and a laptop run exactly the same packages. Useful on
Windows (without WSL2), or as a fallback on Apple Silicon if Rosetta 2 is
not available.

    docker build --platform linux/amd64 -f containers/Dockerfile -t amr-pipeline:1.0.0 .
    pixi run download                      # data on the host
    docker run --rm --platform linux/amd64 -v "$PWD":/work -w /work amr-pipeline:1.0.0 snakemake --cores 4

The *Container* GitHub Action builds the image on every release tag and
publishes it as `ghcr.io/vadimg2/snakemake_antibiotic_resistance:<tag>`.
