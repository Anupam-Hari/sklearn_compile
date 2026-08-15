from transpiler.cython.classifier import classify_call


def build_dependency_graph(calls):

    graph = {}

    for call in calls:

        graph[call] = {
            "type": classify_call(call)
        }

    return graph