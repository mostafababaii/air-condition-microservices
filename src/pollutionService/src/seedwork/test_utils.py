import pytest
import uuid


def marks(*args):
    def _(f):
        for mark in args:
            f = getattr(pytest.mark, mark)(f)
        return f

    return _


def generate_uuid() -> str:
    return str(uuid.uuid4())
