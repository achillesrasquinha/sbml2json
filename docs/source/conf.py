import sys
import os, os.path as osp
import datetime as dt

def pardir(path, level = 1):
    for _ in range(level):
        path = osp.dirname(path)
    return path

BASEDIR = osp.abspath(pardir(__file__, 2))
NOW     = dt.datetime.now()

sys.path.insert(0, BASEDIR)

import sbml2json

project   = sbml2json.__name__
author    = sbml2json.__author__
copyright = "%s %s" % (NOW.year, sbml2json.__author__)

version   = sbml2json.__version__
release   = sbml2json.__version__

source_suffix  = ".md"
source_parsers = { ".md": "recommonmark.parser.CommonMarkParser" } 

master_doc     = "index"