# -*- coding: utf-8 -*-
import ast
import csv
import sys
import tokenize
from collections import Counter
from pathlib import Path

import click
import nbformat
from tqdm import tqdm


def token_distribution(python_file, frequencies):
    """Count token frequency in file

    Args:
        file (string): File to parse
        frequencies (collections.Counter): Counter to add counts
    """
    with open(python_file, 'br') as f:
        for tok in tokenize.tokenize(f.readline):
            frequencies[tok.string] += 1


def count_levels(python_file, output):
    """Count size and number of classes and functions by inspecting the AST.

    Args:
        python_file (string): File to parse
        output (object): csv.writer object
    """
    try:
        with tokenize.open(python_file) as source:
            try:
                tree = ast.parse(source.read())
                classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
                for myclass in classes:
                    functions = myclass.body
                    class_lines = myclass.end_lineno - myclass.lineno + 1
                    for function in functions:
                        if (isinstance(function,
                                       ast.FunctionDef)
                            or isinstance(function,
                                          ast.AsyncFunctionDef)):
                            output.writerow([str(python_file),
                                             myclass.name,
                                             str(class_lines),
                                             function.name,
                                             str(function.end_lineno
                                                 - function.lineno + 1)]
                                            )
            except SyntaxError:
                print(f"skipping {python_file}", file=sys.stderr)
    except SyntaxError:
        print(f"skipping {python_file} tokenize error!", file=sys.stderr)


def parse_notebooks(notebook_file, output):
    try:
        notebook_object = nbformat.read(notebook_file, as_version=4)
        for cell in notebook_object.cells:
            if 'source' in cell:
                output.writerow([notebook_file,
                                 len(cell.source.split('\n')),
                                 cell.cell_type])
    except nbformat.reader.NotJSONError:
        print(f"skipping {notebook_file}", file=sys.stderr)


@click.command()
@click.option('--input_path', default='/mnt/Data/scratch',
              help='Path where input will be scanned recursively')
@click.option('--output', default='python_data.tsv', help='Output file')
@click.option('--method', type=click.Choice(['levels', 'tokens', 'cells']),
              default='levels', help='[levels|tokens|cells]')
def count(input_path, output, method):
    """Count levels or tokens in multiple repositories

    Example usage:

    pycodeseq --input_path /mnt/Data/scratch --output data.tsv --method levels

    """
    with open(output, 'w') as data_file:
        outwriter = csv.writer(data_file, delimiter="\t", lineterminator="\n")
        header = []
        if method == "levels":
            header = ['file', 'class', 'class_lines', 'function',
                      'function_lines']
            extension = ".py"
        elif method == "tokens":
            header = ['rank', 'token_length', 'counts']
            extension = "py"
        elif method == "cells":
            header = ['file', 'cell_lines', 'cell_type']
            extension = "ipynb"
        else:
            print("Unknown method")
        outwriter.writerow(header)
        for python_file in tqdm(list(Path(input_path).glob(f"**/*{extension}"))):
            if not python_file.is_file():
                continue
            if method == "levels":
                count_levels(python_file, outwriter)
            elif method == "tokens":
                frequencies = Counter()
                token_distribution(python_file, frequencies)
            elif method == "cells":
                parse_notebooks(python_file, outwriter)
        if method == "tokens":
            for i, (key, value) in enumerate(frequencies.most_common()):
                outwriter.writerow([i, len(key), value])
