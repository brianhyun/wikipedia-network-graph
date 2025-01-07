import community
import networkx as nx

def dict_to_networkx(graph_dict):
    G = nx.Graph()
    for node in graph_dict["nodes"]:
        G.add_node(node["id"])
    for link in graph_dict["links"]:
        G.add_edge(link["source"], link["target"])
    return G

def detect_communities(graph_dict):
    G = dict_to_networkx(graph_dict)

    # Use Louvain Modularity to detect communities
    partition = community.best_partition(G)

    # Add community info back to nodes
    for node in graph_dict["nodes"]:
        node["community"] = partition[node["id"]]

    return graph_dict