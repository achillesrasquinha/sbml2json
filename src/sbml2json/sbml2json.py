import libsbml

def sbml2json(f):
    dict_ = { }

    reader      = libsbml.Reader()
    document    = reader.readSBML(f)
    model       = document.getModel()

    dict_["id"]     = model.getId()
    dict_["name"]   = model.getName()  

    return dict_