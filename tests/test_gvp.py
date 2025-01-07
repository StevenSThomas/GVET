from gvet.gvp.services import QueryService
from gvet.gvp.services import parse_subject
from gvet.gvp.dataclasses import SubjectType


# def test_query():
#     t = HttpTransport()
#     result = t.execute_query("""
#          select ?id ?label ?note ?type ?parent_string WHERE {
#             ?subject gvp:broader aat:300264086;
#                 skos:inScheme aat:;
#                 dc:identifier ?id;
#                 gvp:prefLabelGVP/xl:literalForm ?label;
#                 skos:scopeNote [dct:language gvp_lang:en; rdf:value ?note];
#                 gvp:parentString ?parent_string;
#                 a ?typ.
#             ?typ rdfs:subClassOf gvp:Subject; rdfs:label ?type.
#           filter (?typ != gvp:Subject)
#         }
#     """)
#     print(result)


def test_get_facets():
    qs = QueryService()
    facets = qs.get_facets()
    assert facets


def test_get_subject_members():
    qs = QueryService()
    subjects = qs.get_subject_members("aat:300264092")
    assert len(subjects) == 9


def test_can_parse_subject():
    """
    Tests that the expected output from a sparql query returning subject information is parsed correctly.
    """
    facet_raw = {
        "id": {"type": "literal", "value": "300264092"},
        "label": {"xml:lang": "en", "type": "literal", "value": "Objects Facet"},
        "note": {
            "xml:lang": "en",
            "type": "literal",
            "value": "Includes terms for discrete tangible or visible things that are inanimate and produced by human endeavor; that is, that are either fabricated or given form by human activity. These range, in physical form, from built works to images and written documents. They range in purpose from utilitarian to the aesthetic. Also included are landscape features that provide the context for the built environment  paintings, amphorae, facades, cathedrals, Brewster chairs, gardens.",
        },
        "type": {"type": "literal", "value": "Facet"},
        "parent_string": {"value": "Top of the AAT hierarchies"},
    }
    facet = parse_subject(facet_raw)
    assert facet.id == "aat:300264092"
    assert facet.label == "Objects Facet"
    assert (
        facet.note
        == "Includes terms for discrete tangible or visible things that are inanimate and produced by human endeavor; that is, that are either fabricated or given form by human activity. These range, in physical form, from built works to images and written documents. They range in purpose from utilitarian to the aesthetic. Also included are landscape features that provide the context for the built environment  paintings, amphorae, facades, cathedrals, Brewster chairs, gardens."
    )
    assert facet.type == SubjectType.FACET
