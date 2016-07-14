from app import cred
from libs.constants import GRAPH_EP


def graph(endpoint):
    return '%s/%s%s' % (GRAPH_EP, cred['tenant'], endpoint)
