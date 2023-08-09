
# getRTax: a tool to extract reads from specific taxonomic groups from BAM files


[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/genomewalker/get-reads-taxonomy?include_prereleases&label=version)](https://github.com/genomewalker/get-reads-taxonomy/releases) [![get-reads-taxonomy](https://github.com/genomewalker/get-reads-taxonomy/workflows/getRTax_ci/badge.svg)](https://github.com/genomewalker/get-reads-taxonomy/actions) [![PyPI](https://img.shields.io/pypi/v/get-reads-taxonomy)](https://pypi.org/project/get-reads-taxonomy/) [![Conda](https://img.shields.io/conda/v/genomewalker/get-reads-taxonomy)](https://anaconda.org/genomewalker/get-reads-taxonomy)

A simple tool to extract reads from specific taxonomic groups BAM files

# Installation

We recommend having [**conda**](https://docs.conda.io/en/latest/) installed to manage the virtual environments

### Using pip

First, we create a conda virtual environment with:

```bash
wget https://raw.githubusercontent.com/genomewalker/get-reads-taxonomy/master/environment.yml
conda env create -f environment.yml
```

Then we proceed to install using pip:

```bash
pip install get-reads-taxonomy
```

### Using mamba

```bash
mamba install -c conda-forge -c bioconda -c genomewalker get-reads-taxonomy
```

### Install from source to use the development version

Using pip

```bash
pip install git+ssh://git@github.com/genomewalker/get-reads-taxonomy.git
```

By cloning in a dedicated conda environment

```bash
git clone git@github.com:genomewalker/get-reads-taxonomy.git
cd get-reads-taxonomy
conda env create -f environment.yml
conda activate get-reads-taxonomy
pip install -e .
```


# Usage

getRTax will take a BAM file and a taxonomy TSV file and extract the reads that map to each of the selected taxa. One can select a list of taxa and ranks to extract the reads from.

For a complete list of options:

```bash
$ getRTax --help
usage: getRTax [-h] -b BAM [-p PREFIX] [--only-read-ids] [--combine] [--unique] -T
               TAXONOMY_FILE -r RANK [-M SORT_MEMORY] [-t THREADS] [--chunk-size CHUNK_SIZE]
               [--debug] [--version]

A simple tool to extract damaged reads from BAM files

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  -b BAM, --bam BAM     The BAM file used to generate the metaDMG results (default: None)

optional arguments:
  -p PREFIX, --prefix PREFIX
                        Prefix used for the output files (default: None)
  --only-read-ids       Only output read IDs instead of the full read (default: False)
  --combine             Combine reads from different taxonomic groups into one file (default:
                        False)
  --unique              Only output unique mapping reads in the case of reads mapping to
                        multiple references (default: False)
  -T TAXONOMY_FILE, --taxonomy-file TAXONOMY_FILE
                        A file containing the taxonomy of the BAM references in the format
                        d__;p__;c__;o__;f__;g__;s__. (default: None)
  -r RANK, --rank RANK  Which taxonomic group and rank we want to get the reads extracted.
                        (default: None)
  -M SORT_MEMORY, --sort-memory SORT_MEMORY
                        Set maximum memory per thread for sorting; suffix K/M/G recognized
                        (default: 1G)
  -t THREADS, --threads THREADS
                        Number of threads (default: 1)
  --chunk-size CHUNK_SIZE
                        Chunk size for parallel processing (default: None)
  --debug               Print debug messages (default: False)
  --version             Print program version
```

One would run `getRTax` as:

```bash
getRTax --bam MED-2021-28-ver15-2LFQY-210811_S25.dedup.bam -T hires-organelles-viruses-smags.tax.tsv -r '{"domain":["d__Bacteria", "d__Archaea", "d__Viruses", "d__Eukaryota"]}' --threads 8 --unique
```
> **Note**: The final number number of reads might not correspond to the number of reads in the BAM file. The reason is that if you are allowing multiple alignments for each read, the reads might be mapped to multiple references. In this case, the reads will be counted multiple times, for example, a read might map to a certain references, but also map to a reference that might be discarded. In this case, the read will be counted twice, once for the reference that is not discarded and once for the reference that is discarded. If you want to avoid this, you can use the `--unique` option, which will only count the read once.

# Using taxonomies
To be able to extract reads from specific taxa and/or ranks, one needs to provide a taxonomy file. This file should be a TSV file with the following format:

```
ACCESSION\td__Bacteria;l__Bacteria;k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Enterobacterales;f__Enterobacteriaceae;g__Yersinia;s__Yersinia pestis
```

`ACCESSION` is the reference accession in the BAM file. The taxonomy is separated by `;` and the taxonomic groups are separated by `__`. The taxonomic groups recognized by `getRTax` in `--taxonomy-file` and `--rank` are:
  - **domain**: `d__`
  - **lineage**: `l__`
  - **kingdom**: `k__`
  - **phylum**: `p__`
  - **class**: `c__`
  - **order**: `o__`
  - **family**: `f__`
  - **genus**: `g__`
  - **species**: `s__`

> **Note**: The taxonomic groups are case sensitive and one can include as many as desired. For example, if one wants to extract the reads from the genus *Yersinia* and the class *Bacilli*, one would use `--rank '{"genus": "Yersinia", "class":"Bacilli"}`.



