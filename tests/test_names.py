import pytest
import project1
from project1 import main

def test_names():
    results = main.main(["tests/flood.txt"], "files/", True, False, False, False, False, "stdout")
    assert results[0] == 26
