from __future__ import absolute_import

import os.path as osp

from testutils import PATH

from sbml2json import sbml2json

PATH["SBML"] = osp.join(PATH["DATA"], "sbml")

def test_sbml2json():
    path_ecoli  = osp.join(PATH["SBML"], "e_coli_core.xml.gz")
    model       = sbml2json(path_ecoli)
    
    assert model["id"]              == "e_coli_core"
    assert model["name"]            == ""
    assert model["compartments"]    == { "e": "extracellular space", "c": "cytosol" }

    path_nave2018   = osp.join(PATH["SBML"], "nave2018.xml")
    model           = sbml2json(path_nave2018)

    assert model["id"]              == "New_Model"

def test_sbml2json_url():
    model = sbml2json("http://bigg.ucsd.edu/static/models/iAB_RBC_283.xml.gz")

    # assert model[]
