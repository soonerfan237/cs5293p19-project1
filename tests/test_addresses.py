import pytest
import project1
from project1 import main

def test_addresses():
    results = main.main(["tests/flood.txt"], "files/", True, True, False, True, False, "stdout")
    assert results[3] == 0
