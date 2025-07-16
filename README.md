# PLINKLiftOver

[![Build status](https://github.com/milescsmith/plinkliftover/workflows/build/badge.svg?branch=master&event=push)](https://github.com/milescsmith/plinkliftover/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/plinkliftover.svg)](https://pypi.org/project/plinkliftover/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/milescsmith/plinkliftover/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/milescsmith/plinkliftover/releases)
[![License](https://img.shields.io/github/license/milescsmith/plinkliftover)](https://github.com/milescsmith/plinkliftover/blob/master/LICENSE)
![Alt](https://repobeats.axiom.co/api/embed/8d9c682229fb45f45eef3f300367eb33a44bd347.svg "Repobeats analytics image")

**PLINKLiftOver** is a utility enabling [liftOver](http://genome.ucsc.edu/cgi-bin/hgLiftOver)
to work on genomics files from [PLINK](https://www.cog-genomics.org/plink/),
allowing one to update the coordinates from one genome reference version to
another.


## Installation

PLINKLiftOver requires
* Python 3.10
* The command line version of [liftOver](http://genome.ucsc.edu/cgi-bin/hgLiftOver),
installed and on the system path
* An appropriate [chain file](http://hgdownload.soe.ucsc.edu/downloads.html#liftover)
* The [MAP file](https://zzz.bwh.harvard.edu/plink/data.shtml) from a PLINK
dataset

Install from [pypi](https://pypi.org/project/plinkliftover/)
```bash
pip install -U plinkliftover
```

or install the development version with

```bash
pip install -U git+https://github.com/milescsmith/plinkliftover.git
```

## Usage

plinkliftover has three subcommands:
* liftover: Fully convert the genomic coordinates from one version to another 
in a PLINK file
* map2bed: Convert a PLINK MAP file to a BED file
* bed2map: Convert a BED file to a MAP file

The latter two subcommands are most useful in situations where it is not 
possible to run the liftOver executable locally (i.e. you are on Windows) but 
can use [UCSC's online version](https://genome.ucsc.edu/cgi-bin/hgLiftOver) 
or you otherwise need/want a BED file.


### liftover:

```bash
Usage: plinkliftover liftover [OPTIONS] MAPFILE CHAINFILE

  Converts genotype data stored in the PLINK PED+MAP format from one genome
  build to another, using liftOver.

Arguments:
  MAPFILE    The plink MAP file to `liftOver`.  [required]
  CHAINFILE  The location of the chain files to provide to `liftOver`.
             [required]

Options:
  --pedfile TEXT             Optionally remove "unlifted SNPs" from the plink
                             PED file after running `liftOver`.
  --datfile TEXT             Optionally remove 'unlifted SNPs' from a data
                             file containing a list of SNPs (e.g. for
                             --exclude or --include in `plink`)
  --prefix TEXT              The prefix to give to the output files.
  --liftoverexecutable TEXT  The location of the `liftOver` executable.
  -v, --version              Prints the version of the plinkliftover package.
  --help                     Show this message and exit.
```

For example

```bash
plinkliftover liftover updating.map hg19ToHg38.over.chain.gz --prefix updated
```

### map2bed:

```bash
Usage: plinkliftover map2bed [OPTIONS] MAPFILE

  Convert genotype data stored in a PLINK MAP file into a BED file, allowing
  one to use the online version of liftOver should the local executable is
  unavailable

Arguments:
  MAPFILE  A PLINK MAP file.  [required]

Options:
  -o, --output PATH  Location to save BED file to.  If one is not provided,
                     then it will be saved to where the MAP file is.
  -v, --version      Prints the version of the plinkliftover package.
  --help             Show this message and exit.
```

### bed2map:

```bash
Usage: plinkliftover bed2map [OPTIONS] BEDFILE

  Convert genotype data stored in a PLINK MAP file into a BED file, allowing
  one to use the online version of liftOver should the local executable is
  unavailable

Arguments:
  BEDFILE  A BED file.  [required]

Options:
  -o, --output PATH  Location to save MAP file to.  If one is not provided,
                     then it will be saved to where the BED file is.
  -v, --version      Prints the version of the plinkliftover package.
  --help             Show this message and exit.
```

### Note!

By default, [PLINK 2.0](https://www.cog-genomics.org/plink/2.0/) does not 
use/create the required MAP file.  It can be generated using PLINK 1.9 by

```bash
plink --bfile original --recode --out to_update
```

where `original` is the prefix for the bed/bim/fam files and `to_update` is the prefix to give the new files.

## 🛡 License

[![License](https://img.shields.io/github/license/milescsmith/plinkliftover)](https://github.com/milescsmith/plinkliftover/blob/master/LICENSE)

This project is licensed under the terms of the `GNU GPL v3.0` license. See [LICENSE](https://github.com/milescsmith/plinkliftover/blob/master/LICENSE) for more details.

## 📃 Citation

```
@misc{plinkliftover,
  author = {Miles Smith <miles-smith@omrf.org>},
  title = {Awesome `plinkliftover` is a Python cli/package created with https://github.com/TezRomacH/python-package-template},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/milescsmith/plinkliftover}}
}
```

## Credits

This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template).
