"""
Unit and regression test for the hoatzin package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import hoatzin


def test_hoatzin_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "hoatzin" in sys.modules
