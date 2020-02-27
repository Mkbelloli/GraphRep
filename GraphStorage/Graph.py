import networkx
from Utils.functionsLib import *


class EntityPeriodGraph:
    def __init__(self, entity, period):
        self.entity_name = entity
        self.reported_period = period
        self.graph = networkx.MultiGraph()

    def update_dp(self, tid, dp_name, dp_value):

        if not self.graph.has_node(dp_name):
            self.graph.add_node(dp_name)

        self.graph.nodes[dp_name][float(tid)] = dp_value

    def get_dp_value(self,dp_name):
        if not self.graph.has_node(dp_name):
            return None

        last_tid = list(self.graph[dp_name].keys()).sort()[-1]
        return self.graph.nodes[dp_name][last_tid]

    def print(self):
        print("--------------------------------")
        print("ENTITY:{}".format(self.entity_name))
        print("REPORTED PERIOD:{}".format(self.reported_period))

        for node in self.graph.nodes.keys():
            print("DataPoint:{}".format(node))
            for tid, value in self.graph.nodes[node].items():
                print("tid:{} value:{}".format(tid, value))
        print("--------------------------------")


class EntityGraph:
    def __init__(self, entity):
        self.entity_name = entity
        self.graph = networkx.Graph()
        self.__initialize__()

    def __initialize__(self):
        self.add_check("C01.00_r330_c010", "C01.00_r230_c010", positiveValue)

    def update_dp(self, rep_period, tid, dp_name, dp_value):
        if not self.graph.has_node(dp_name):
            self.graph.add_node(dp_name)

        if rep_period not in self.graph.nodes[dp_name].keys():
            self.graph.nodes[dp_name][rep_period] = {}

        self.graph.nodes[dp_name][rep_period][float(tid)] = dp_value

    def add_check(self, nodeA, nodeB, funct):
        if nodeA not in self.graph.nodes.keys() :
            self.graph.add_node(nodeA)

        if nodeB not in self.graph.nodes.keys():
            self.graph.add_node(nodeB)

        if (nodeA, nodeB) not in self.graph.edges.keys():
            self.graph.add_edge(nodeA, nodeB)

        self.graph.edges[(nodeA, nodeB)]['func'] = funct

    def get_dp_value(self, rep_period, dp_name):
        if not self.graph.has_node(dp_name):
            return None

        if rep_period not in self.graph.nodes[dp_name].keys():
            return None

        last_tid = max(list(self.graph.nodes[dp_name][rep_period].keys()))
        return self.graph.nodes[dp_name][rep_period][last_tid]

    def print(self):
        print("--------------------------------")
        print("ENTITY:{}".format(self.entity_name))

        for node in self.graph.nodes.keys():
            print("DataPoint:{}".format(node))
            for rep_period in self.graph.nodes[node].keys():
                for tid, value in self.graph.nodes[node][rep_period].items():
                    print("rep:{} tid:{} value:{}".format(rep_period, tid, value))
        print("--------------------------------")

    def check(self, rep_period):
        for e in self.graph.edges:
            self.graph.edges[e]["func"](rep_period, self, e[0], e[1])