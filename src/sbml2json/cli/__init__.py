# imports - module imports
from sbml2json.cli.util   import *
from sbml2json.cli.parser import get_args
from sbml2json.util._dict import merge_dict
from sbml2json.util.types import get_function_arguments

def command(fn):
    args    = get_args()
    
    params  = get_function_arguments(fn)

    params  = merge_dict(params, args)
    
    def wrapper(*args, **kwargs):
        return fn(**params)

    return wrapper