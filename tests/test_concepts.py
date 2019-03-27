import pytest
import project1
from project1 import main

def test_concept_flood():
    results = main.main(["tests/flood.txt"], "files/", True, True, True, True, True, "stdout",["flood"])
    assert results[5] == [7]

def test_concept_report():
    results = main.main(["tests/mueller.txt"], "files/", True, True, True, True, True, "stdout",["report"])
    assert results[5] == [8]

