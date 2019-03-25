import pytest
import project1
from project1 import main

def test_dates():
    results = main.main(["tests/flood.txt"], "files/", False, False, True, False, False, "stdout")
    assert results[2] == 4
