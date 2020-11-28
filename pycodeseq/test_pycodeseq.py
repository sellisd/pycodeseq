# -*- coding: utf-8 -*-
import csv
import filecmp
import json
from collections import Counter

import pytest
from click.testing import CliRunner

import pycodeseq


def test_token_distribution():
    frequencies = Counter()
    python_file = './test_data/class_example.py'
    pycodeseq.token_distribution(python_file, frequencies)
    with open('./test_data/class_example_tokens.json', 'r') as f:
        r = json.load(f)
    assert(frequencies == r)


def test_count_levels(tmp_path):
    input_file = './test_data/class_example.py'
    output_file = tmp_path / 'levels_output.tsv'
    template_output_file = './test_data/count_levels_example.tsv'
    with open(output_file, 'w') as f:
        outwriter = csv.writer(f, delimiter="\t", lineterminator="\n")
        pycodeseq.count_levels(input_file, outwriter)
    assert(filecmp.cmp(output_file, template_output_file, shallow=False))


def test_parse_notebooks(tmp_path):
    input_file = './test_data/notebook_example.ipynb'
    output_file = tmp_path / 'cells_output.tsv'
    template_output_file = './test_data/notebook_example.tsv'
    with open(output_file, 'w') as f:
        outwriter = csv.writer(f, delimiter="\t", lineterminator="\n")
        pycodeseq.parse_notebooks(input_file, outwriter)
    assert(filecmp.cmp(output_file, template_output_file, shallow=False))


@pytest.mark.parametrize("method, template_output_file",
                         [("levels", "./test_data/test_count_levels.tsv"),
                          ("cells", "./test_data/test_count_cells.tsv"),
                          ("tokens", "./test_data/test_count_tokens.tsv")])
def test_count(tmp_path, method, template_output_file):
    runner = CliRunner()
    input_path = './test_data/'
    output_file = tmp_path / 'data.tsv'
    ressults = runner.invoke(pycodeseq.count, ['--input_path', input_path,
                                               '--output', output_file,
                                               '--method', method])
    assert(filecmp.cmp(output_file, template_output_file, shallow=False))
