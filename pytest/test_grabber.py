import sys
import pytest

sys.path.append('../grabber/')

from grabber import insert_current_values


def test_equality():
    assert 11 == 11
