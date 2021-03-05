# -*- coding: utf-8 -*-
import csv
import json
from collections import Counter
from pathlib import Path

import pytest
from click.testing import CliRunner
from pycodeseq import pycodeseq

TEST_DATA_DIR = Path(__file__).resolve().parent / 'test_data'


def test_token_distribution():
    frequencies = Counter()
    python_file = TEST_DATA_DIR / 'class_example.py'
    pycodeseq.token_distribution(python_file, frequencies)
    with open(TEST_DATA_DIR / 'class_example_tokens.json', 'r') as f:
        r = json.load(f)
    assert(frequencies == r)


def test_count_levels(tmp_path):
    input_file = TEST_DATA_DIR / 'class_example.py'
    output_file = tmp_path / 'levels_output.tsv'
    template_output_file = TEST_DATA_DIR / 'count_levels_example.tsv'
    with open(output_file, 'w') as f:
        outwriter = csv.writer(f, delimiter="\t", lineterminator="\n")
        pycodeseq.count_levels(input_file, outwriter)
    assert(compare_columns(output_file, template_output_file))


def test_parse_notebooks(tmp_path):
    input_file = TEST_DATA_DIR / 'notebook_example.ipynb'
    output_file = tmp_path / 'cells_output.tsv'
    template_output_file = TEST_DATA_DIR / 'notebook_example.tsv'
    with open(output_file, 'w') as f:
        outwriter = csv.writer(f, delimiter="\t", lineterminator="\n")
        pycodeseq.parse_notebooks(input_file, outwriter)
    assert(compare_columns(output_file, template_output_file))


@pytest.mark.parametrize("method, template_output_file",
                         [("levels", TEST_DATA_DIR / "test_count_levels.tsv"),
                          ("cells", TEST_DATA_DIR / "test_count_cells.tsv"),
                          ("tokens", TEST_DATA_DIR / "test_count_tokens.tsv")])
def test_count(tmp_path, method, template_output_file):
    runner = CliRunner()
    input_path = TEST_DATA_DIR
    output_file = tmp_path / 'data.tsv'
    runner.invoke(pycodeseq.count, ['--input_path', input_path,
                                    '--output', output_file,
                                    '--method', method])
    assert(compare_columns(output_file, template_output_file))


def compare_columns(file1, file2):
    with open(file1, 'r') as f1:
        with open(file2, 'r') as f2:
            l1 = f1.readline().split("\t")
            l2 = f2.readline().split("\t")
            if l1[1:] != l2[1:]:
                return False
    return True
