import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from unittest.mock import patch

import pytest

from api.helper import valid_password

def test_valid_password():
    test = "Tcool231@s"
    valid = valid_password(test)
    assert valid == True

def test_invalid_password_not_str():
    numbers = 333312
    with pytest.raises(ValueError):
        valid_password(numbers)

def test_invalid_password_1():
    test = "Tcoos"
    valid = valid_password(test)
    assert valid == False

def test_invalid_password_2():
    test = "Tcoo23s99"
    valid = valid_password(test)
    assert valid == False

def test_invalid_password_3():
    test = "amid@ingth1swright?"
    valid = valid_password(test)
    assert valid == False

def test_invalid_password_4():
    test = "TrueGaming123"
    valid = valid_password(test)
    assert valid == False

def test_invalid_password_5():
    test = "Is this 1 sentance or many?"
    valid = valid_password(test)
    assert valid == False