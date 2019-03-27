import pytest
import project1
from project1 import main

def test_genders(): 
    results = main.main(["tests/flood.txt"], "files/", True, True, True, True, True, "stdout",[])
    assert results[1] == 49
