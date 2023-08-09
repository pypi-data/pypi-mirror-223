"""CLiSN - Namespaces and custom NamespaceManager for CLSInfra."""

import sys

from rdflib import Graph, Namespace
from rdflib.namespace import NamespaceManager
from rdflib._type_checking import _NamespaceSetString


# namespaces
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
crmcls = Namespace("https://clscor.io/ontologies/CRMcls/")
clst = Namespace("https://core.clscor.io/entity/type/")
clscore = Namespace("https://core.clscor.io/entity/")
frbr = Namespace("https://cidoc-crm.org/frbroo/")
crmdig = Namespace("https://cidoc-crm.org/crmdig/")
lrm = Namespace("http://www.cidoc-crm.org/lrmoo/")
pem = Namespace("http://parthenos.d4science.org/CRMext/CRMpe.rdfs")


def corpus_base(corpus_key: str) -> Namespace:
    """Generate a corpus base URI given a corpus_key (the corpus acronym).

    Pattern: https://{corpus_key}.clscor.io/entity/{entity-type}/{hash-id}.
    """
    corpus_key = corpus_key.lower()

    return Namespace(f"https://{corpus_key}.clscor.io/entity/")


namespaces = {
    key: value for key, value
    in sys.modules[__name__].__dict__.items()
    if isinstance(value, Namespace)
}


class CLSInfraNamespaceManager(NamespaceManager):
    """Custom NamespaceManager for CLSInfra.

    Useage e.g. for creating a namespaced graph:
    ```
    graph = rdflib.Graph
    clisn.CLSInfraNamespaceManager(graph)
    ```
    """

    def __init__(self,
                 graph: Graph,
                 bind_namespaces: "_NamespaceSetString" = "rdflib"):
        """Call init.super and add CLSInfra namespaces."""
        super().__init__(graph=graph, bind_namespaces=bind_namespaces)

        for prefix, ns in namespaces.items():
            graph.bind(prefix, ns)
