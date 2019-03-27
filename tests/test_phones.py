import pytest
import project1
from project1 import main

def test_phones():
    results = main.main(["tests/phones.txt"], "files/", True, True, True, True, True, "stdout",[])
    assert results[4] == 3
