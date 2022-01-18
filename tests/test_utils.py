import os

import pytest

from fastack.utils import load_app


def test_fail_load_app():
    os.environ.pop("FASTACK_APP", None)
    with pytest.raises(RuntimeError, match='If you use the "fastack" command'):
        load_app()
