import pytest
import project1
from project1 import main

def test_addresses():
    results = main.main(["tests/addresses.txt"], "files/", True, True, True, True, True, "stdout",[])
    assert results[3] == 3
