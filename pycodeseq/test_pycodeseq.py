import pytest
from collections import Counter
import pycodeseq
import json


def test_token_distribution():
    frequencies = Counter()
    python_file = './test_data/class_example.py'
    pycodeseq.token_distribution(python_file, frequencies)
    with open('./test_data/class_example_tokens.json', 'r') as f:
        r = json.load(f)
    assert(frequencies == r)