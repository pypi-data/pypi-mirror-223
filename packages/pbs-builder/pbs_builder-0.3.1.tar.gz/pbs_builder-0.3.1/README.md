# PBS-builder

A simplified version of workflow management system for scalable data analysis.

# Change log

- Version 0.3.1: add allocated/total gpus in `pestat` output
- Version 0.3.0: include `pestat` in package data
- Version 0.2.0: move `sample_sheet` from header to job section, add `group_sheet` support.
- Version 0.1.0: first functional version.

# Usage

Please refer to our [wiki](https://bioinfo.biols.ac.cn/git/zhangjy/pbs-builder/wiki/_pages) for detailed instructions.

# Installation

pbs-builder is heavily inspired by Snakemake, but uses native SLURM/Torque dependencies to build analysis pipeline.

pbs-builder runs in **python3.7+** with the `tomli` package installed, no other dependencies are required.

Install pbs-builder using the following command:

```bash
pip install pbs-builder
```
