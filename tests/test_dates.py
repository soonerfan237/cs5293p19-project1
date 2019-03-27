import pytest
import project1
from project1 import main

def test_dates():
    results = main.main(["tests/dates.txt"], "files/", True, True, True, True, True, "stdout",[])
    assert results[2] == 21
