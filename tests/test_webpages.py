import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from unittest.mock import patch

import pytest

from neuro_nuggets.routes.auth import valid_password
from neuro_nuggets.app import app

def test_homepage():
    with app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200

def test_homepage():
    with app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200