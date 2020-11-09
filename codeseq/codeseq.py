import ast
import itertools
import sys
import tokenize
from collections import Counter
from pathlib import Path

import click
import pandas as pd
from tqdm import tqdm

input_path = Path('/mnt/Data/scratch')


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
        output (string): File to append the output
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
                        if isinstance(function,
                                      ast.FunctionDef)
                        or isinstance(function,
                                      ast.AsyncFunctionDef):
                            output.write("\t".join([str(python_file),
                                                    myclass.name,
                                                    str(class_lines),
                                                    function.name,
                                                    str(function.end_lineno
                                                        - function.lineno + 1)]
                                                   )
                                         )
            except SyntaxError:
                print(f"skipping {python_file}", file=sys.stderr)
    except SyntaxError:
        print(f"skipping {python_file} tokenize error!", file=sys.stderr)


@click.command()
@click.option('--output', default='data.tsv', help='Output file')
@click.option('--method', default='levels', help='count levels or tokens')
def count(output, method):
    python_files = Path(input_path).glob("**/*.py")
    if method == "levels":
        with open(output, 'w') as data_file:
            data_file.write("\t".join(['file',
                                       'class',
                                       'class_lines',
                                       'function',
                                       'function_lines']))
            for f in tqdm(python_files):
                if f.is_file():
                    count_levels(f, output)
    elif method == "tokens":
        frequencies = Counter()
        for f in tqdm(python_files):
            if f.is_file():
                token_distribution(f, frequencies)
        with open(output, 'w') as data_file:
            data_file.write("\t".join(['rank',
                                       'token_length',
                                       'counts']))
            for i, (key, value) in enumerate(frequencies.most_common()):
                data_file.write(i, len(key), value, sep="\t")
    else:
        print("Unknown method")
