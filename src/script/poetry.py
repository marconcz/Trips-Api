# This is a temporary workaround till Poetry supports scripts, see
# https://github.com/sdispater/poetry/issues/241.
# Source: https://medium.com/octopus-wealth/python-scripts-26e3d0bd5277

# Standard library imports
from subprocess import check_call


def format() -> None:
    check_call(
        ["black", "--check", "--diff", "src", "test"],
    )


def reformat() -> None:
    check_call(["black", "src", "test"])


def lint() -> None:
    check_call(["flake8", "src", "test"])
    check_call(["mypy", "src", "test"])


def start() -> None:
    check_call(["python", "-m", "src.main"])


def test() -> None:
    check_call(["pytest", "test"])
