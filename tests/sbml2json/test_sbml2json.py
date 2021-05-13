import os.path as osp

from testutils import PATH

from sbml2json import sbml2json

PATH["SBML"] = osp.join(PATH["DATA"], "sbml")

def test_sbml2json():
    path_ecoli  = osp.join(PATH["SBML"], "e_coli_core.xml.gz")
    
    model       = sbml2json(path_ecoli)
    
    assert model == {
        "id": "e_coli_core",
        "name": "",
        "compartments": {
            "e": "extracellular space",
            "c": "cytosol"   
        }
    }