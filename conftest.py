"""Project-wide pytest setup: chooses which gp_em.py the checks import.

    pytest            -> your own gp_em.py in this directory
    pytest --key      -> answer_key/gp_em.py
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent


def pytest_addoption(parser):
    parser.addoption("--key", action="store_true", help="run against answer_key/gp_em.py")


def pytest_configure(config):
    if config.getoption("--key"):
        sys.path.insert(0, str(ROOT / "answer_key"))
    elif not (ROOT / "gp_em.py").exists():
        pytest.exit(
            "No gp_em.py here yet. You write it in worksheet Part 6 "
            "(worksheet/06-implement-naive.md). To see the checks pass against "
            "the answer key, run: pytest --key",
            returncode=1,
        )
