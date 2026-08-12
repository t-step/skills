import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from parser.tokenize import tokenize


def test_basic_expression():
    assert tokenize("12+3 * 45") == ["12", "+", "3", "*", "45"]


def test_single_number():
    assert tokenize("7") == ["7"]


def test_operators_no_spaces():
    assert tokenize("1+2-3") == ["1", "+", "2", "-", "3"]
