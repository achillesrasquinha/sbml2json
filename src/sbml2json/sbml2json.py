from __future__ import absolute_import

import os.path as osp
import re
import gzip

import libsbml

from sbml2json.util.string  import strip
from sbml2json.util.system  import check_gzip, make_temp_dir, write
from sbml2json.util._dict   import merge_dict
from sbml2json.util.request import check_url
from sbml2json.log          import get_logger
from sbml2json              import request as req

logger      = get_logger()

# https://git.io/Jsm7p
REGEX_NOTES = re.compile(
    r"<(?P<prefix>(\w+:)?)p[^>]*>(?P<content>.*?)</(?P=prefix)p>",
    re.IGNORECASE | re.DOTALL,
)

def _get_model(reader, f):
    document    = reader.readSBML(f)
    model       = document.getModel()

    return model

def _get_stoichiometry(species, type_):
    direction = -1 if type_ == "r" else 1
    return dict(
        ( m_species.getSpecies(), m_species.getStoichiometry() * direction )
            for m_species in species
    )

from cobra.io.sbml import _parse_notes_dict as _parse_notes, _parse_annotations

# # https://git.io/Jsm5L
def _parse_notes(sbase):
    notes = sbase.getNotesString()
    dict_ = { }

    if notes and len(notes) > 0:
        dict_ = { }

        for match in REGEX_NOTES.finditer(notes):
            content = match.group("content")

            try:
                key, value = list(map(strip, content.split(":", 1)))
            except ValueError:
                logger.error('Unexpected content format: %s' % content)
                continue

            if value:
                dict_[key] = value

    return dict_

def _parse_annotations(sbase):
    annotations = { }

    # TODO: Implement

    return annotations

def sbml2json(f):
    dict_   = { }
    model   = None
    
    reader  = libsbml.SBMLReader()

    with make_temp_dir() as tmp_dir:
        if check_url(f, raise_err = False):
            response = req.get(f, stream = True)

            if response.ok:
                output_file = osp.join(tmp_dir, "downloaded")

                with open(output_file, mode = "wb") as output_fh:
                    for content in response.iter_content(chunk_size = 1024):
                        if content:
                            output_fh.write(content)

                f = output_file
            else:
                response.raise_for_status()

        if check_gzip(f, raise_err = False):
            with gzip.open(f, "rb") as extracted_file:
                content = extracted_file.read()

                output_file = osp.join(tmp_dir, "output.xml")
                write(output_file, content, mode = "wb")

                model = _get_model(reader, output_file)
        else:
            model = _get_model(reader, f)

    if not model:
        raise ValueError("Unable to read SBML Model from file: %s" % f)

    model_id = model.getIdAttribute()

    metadata = { }

    metadata["level"]   = model.getLevel()
    metadata["version"] = model.getVersion()

    # TODO: Check parsing
    # metadata["notes"]   = _parse_notes(model)

    annotations             = _parse_annotations(model)
    dict_["annotations"]    = annotations

    dict_["id"]     = model_id
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
        reactions.append({
            "id":           m_reaction.getId(),
            "name":         m_reaction.getName(),
            "stoichiometry": merge_dict(
                _get_stoichiometry(m_reaction.getListOfReactants(), "r"),
                _get_stoichiometry(m_reaction.getListOfProducts(),  "p")
            )
        })

    dict_["reactions"]  = reactions

    dict_["_meta"]      = metadata

    return dict_