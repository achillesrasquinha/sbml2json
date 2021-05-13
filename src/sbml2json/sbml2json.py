from __future__ import absolute_import

import os.path as osp
import gzip

import libsbml

from sbml2json.util.system import check_gzip, make_temp_dir, write
from sbml2json.util._dict  import merge_dict

def _get_model(reader, f):
    document    = reader.readSBML(f)
    model       = document.getModel()

    return model

def _get_stoichiometry(species, reversible):
    direction = -1 if reversible else 1

    return dict(
        ( m_species.getSpecies(), m_species.getStoichiometry() * direction )
            for m_species in species
    )

def sbml2json(f):
    dict_   = { }
    model   = None
    
    reader  = libsbml.SBMLReader()

    if check_gzip(f, raise_err = False):
        with gzip.open(f, "rb") as extracted_file:
            content = extracted_file.read()

            with make_temp_dir() as tmp_dir:
                output_file = osp.join(tmp_dir, "output.xml")
                write(output_file, content, mode = "wb")

                model = _get_model(reader, output_file)
    else:
        model = _get_model(reader, f)

    if not model:
        raise ValueError("Unable to read SBML Model from file: %s" % f)

    dict_["id"]     = model.getId()
    dict_["name"]   = model.getName()

    compartments    = { }

    for m_compartment in model.getListOfCompartments():
        compartments[ m_compartment.getId() ] = m_compartment.getName()

    dict_["compartments"] = compartments

    species = [ ]

    for m_species in model.getListOfSpecies():
        species.append({
            "id":           m_species.getId(),
            "name":         m_species.getName(),
            "compartment":  m_species.getCompartment()
        })
        
    dict_["species"] = species

    reactions = [ ]

    for m_reaction in model.getListOfReactions():
        reversible = m_reaction.getReversible()
        
        reactions.append({
            "id":           m_reaction.getId(),
            "name":         m_reaction.getName(),
            "stoichiometry":    merge_dict(
                _get_stoichiometry(m_reaction.getListOfReactants(), reversible),
                _get_stoichiometry(m_reaction.getListOfProducts(), reversible)
            )
        })

    dict_["reactions"]  = reactions

    return dict_
