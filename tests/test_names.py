import pytest
import project1
from project1 import main

def test_names():
    results = main.main(["tests/mueller.txt"], "files/", True, True, True, True, True, "stdout",[])
    assert results[0] == 33
