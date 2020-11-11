import ast
import csv
import itertools
import sys
import tokenize
from collections import Counter
from pathlib import Path

import click
import pandas as pd
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
    """Count number of classes functions and lines of code in function

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
                    class_lines = myclass.end_lineno - myclass.lineno
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


@click.command()
@click.option('--input_path', default='/mnt/Data/scratch',
              help='Path where input will be scanned recursively')
@click.option('--output', default='data.tsv', help='Output file')
@click.option('--method', default='levels', help='[levels|tokens]')
def count(input_path, output, method):
    """Count levels or tokens in multiple repositories

    Example usage:

    codeseq --input_path /mnt/Data/scratch --output data.tsv --method levels

    """
    with open(output, 'w', newline='') as data_file:
        outwriter = csv.writer(data_file, delimiter="\t")
        header = []
        if method == "levels":
            header = ['file', 'class', 'class_lines', 'function',
                      'function_lines']
        elif method == "tokens":
            header = ['rank', 'token_length', 'counts']
        else:
            print("Unknown method")
        outwriter.writerow(header)
        for repository_owner in tqdm(list(Path(input_path).iterdir())):
            for repository_dir in repository_owner.iterdir():
                python_files = Path(repository_dir).glob("**/*.py")
                if method == "levels":
                    for f in python_files:
                        if f.is_file():
                            count_levels(f, outwriter)
                elif method == "tokens":
                    frequencies = Counter()
                    for f in python_files:
                        if f.is_file():
                            token_distribution(f, frequencies)
                        for i, (key, value) in enumerate(frequencies.most_common()):
                            outwriter.writerow([i, len(key), value])
