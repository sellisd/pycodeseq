# A tool for extracting statistics from python ASTs (Abstract Syntax Trees) and jupyter notebooks

A command line program that recursively processes files to find either python scripts or jupyter notebooks and processes them to extract statistics. Python scripts and jupyter notebooks are treated in a very different maner.

From jupyter notebooks the size in terms of lines of code of code or markdown cells are aggregated across all files. For Python scripts there are two different options either aggregate the token rank and frequency distribution or calculate the size (in terms of lines of code) of all classes and functions in the scripts.

## Installing / Getting started

```shell
python -m pip install clone git+https://github.com/sellisd/pycodeseq.git@main
```

To parse the ASTs in all python files found under `pyrepository` use the following:

```shell
pycodeseq --input_path pyrepository --output stats.tsv --method levels
```

To calculate the token rank frequency distribution of all python files under `pyrepository` run:

```shell
pycodeseq --input_path pyrepository --output stats.tsv --method tokens
```

To calculate the size of different types of cells in jupyter notebooks under `pyrepository` run:

```shell
pycodeseq --input_path pyrepository --output stats.tsv --method cells
```

## Developing

To develop it is easier to clone and install editable:

```shell
git clone git@github.com:sellisd/pycodeseq.git
cd pycodeseq/
pip install -e .
```
