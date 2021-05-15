import os.path as osp

# imports - compatibility imports
from sbml2json.commands    import _command as command
from sbml2json.util._dict  import merge_dict
from sbml2json.util.string import strip_ansi

# imports - test imports
import pytest

# imports - test imports
from testutils import mock_input, PATH