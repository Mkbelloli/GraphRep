import networkx

ENTITY_PARAM_NAME = "ENTITY_ID"
TID_PARAM_NAME = "TID_RECEIVED_MODULES"

class GraphGenerator:
    def __init__(self, loader):
        self.loader = loader

    def generate_graphs(self):

        graphs = {}
        entity_name = None
        for p, v in self.loader:
            if p == ENTITY_PARAM_NAME:
                entity_name = v
                continue

            if p == TID_PARAM_NAME:
                tid_name = v
                continue

            if not entity_name in graphs:
                graphs[entity_name] = networkx.Graph()

            gr = graphs[entity_name]

