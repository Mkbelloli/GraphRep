
def positiveValue( rep_period, graph, nodeA, nodeB):
    valueA = graph.get_dp_value(rep_period, nodeA)
    valueB = graph.get_dp_value(rep_period, nodeB)
    if valueA < valueB:
        print("valueA > valueB")