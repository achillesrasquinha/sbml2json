

# imports - standard imports
import subprocess as sp

# imports - module imports
from sbml2json.util.system import popen
from sbml2json.exception   import (
    Sbml2jsonError,
    PopenError
)

# imports - test imports
import pytest

def test_sbml2json_error():
    with pytest.raises(Sbml2jsonError):
        raise Sbml2jsonError

def test_popen_error():
    with pytest.raises(PopenError):
        popen('python -c "raise TypeError"')

    assert isinstance(
        PopenError(0, "echo foobar"),
        (Sbml2jsonError, sp.CalledProcessError)
    )
    assert isinstance(Sbml2jsonError(), Exception)