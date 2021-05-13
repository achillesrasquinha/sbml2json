import os.path as osp

from testutils import PATH

def test_sbml2json():
    path_ecoli = osp.join(PATH["DATA"], "sbml", "e")
