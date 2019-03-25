import pytest
import project1
from project1 import main

def test_genders():
    results = main.main(["tests/flood.txt"], "files/", False, True, False, False, False, "stdout")
    assert results[1] == 52
    #assert 2 == 1
