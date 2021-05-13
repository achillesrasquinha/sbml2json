import os, os.path as osp

import sbml2json
from   sbml2json.util.system import makedirs

class Cache:
    def __init__(self, location = None, dirname = None):
        self.location = location or osp.expanduser("~")
        self.dirname  = dirname  or ".%s" % (sbml2json.__name__)

    def create(self, exist_ok = True):
        path = osp.join(self.location, self.dirname)
        makedirs(path, exist_ok = exist_ok)