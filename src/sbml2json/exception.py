# imports - standard imports
import subprocess as sp

class Sbml2jsonError(Exception):
    pass

class PopenError(Sbml2jsonError, sp.CalledProcessError):
    pass

class DependencyNotFoundError(ImportError):
    pass