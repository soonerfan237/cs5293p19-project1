import pytest
import project1
from project1 import main

def test_phones():
    results = main.main(["tests/phones.txt"], "files/", False, False, False, False, True, "stdout")
    assert results[4] == 3
