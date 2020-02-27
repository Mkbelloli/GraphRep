from GraphStorage.Graph import EntityPeriodGraph, EntityGraph
import pickle
import os
POOL_FILENAME = "graph_pool.pkl"


class EntityPeriodGraphPool:
    def __init__(self):
        self.g_pool = {} # key entity -> reported_period

        if os.path.isfile(POOL_FILENAME):
            with open(POOL_FILENAME, 'rb') as handle:
                self.g_pool = pickle.loads(handle.read())

    def pop_graph(self, entity_key, period_key):

        if entity_key not in self.g_pool:
            self.g_pool[entity_key] = {}

        if period_key not in self.g_pool[entity_key]:
            self.g_pool[entity_key][period_key] = EntityPeriodGraph(entity_key, period_key)

        return self.g_pool[entity_key][period_key]

    def push_graph(self, entity_key, period_key, graph):
        if entity_key not in self.g_pool:
            self.g_pool[entity_key] = {}

        self.g_pool[entity_key][period_key] = graph

    def save(self):
        with open(POOL_FILENAME, 'wb') as handle:
            pickle.dump(self.g_pool, handle)

    def print(self):
        for e in self.g_pool.keys():
            for p in self.g_pool[e]:
                self.g_pool[e][p].print()


class EntityGraphPool:
    def __init__(self):
        self.g_pool = {} # key entity

        if os.path.isfile(POOL_FILENAME):
            with open(POOL_FILENAME, 'rb') as handle:
                self.g_pool = pickle.loads(handle.read())

    def pop_graph(self, entity_key):

        if entity_key not in self.g_pool:
            self.g_pool[entity_key] = EntityGraph(entity_key)

        return self.g_pool[entity_key]

    def push_graph(self, entity_key, graph):
        self.g_pool[entity_key] = graph

    def save(self):
        with open(POOL_FILENAME, 'wb') as handle:
            pickle.dump(self.g_pool, handle)

    def print(self):
        for e in self.g_pool.keys():
            self.g_pool[e].print()

    def check_graphs(self, rep_period):
        for g in self.g_pool.values():
            g.check(rep_period)