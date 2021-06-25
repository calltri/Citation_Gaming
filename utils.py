import pandas as pd
from neo4j import GraphDatabase
import networkx as nx
import tqdm
import pdb

def evaluate_network():
    data = pd.read_csv("criminology_citations.csv", header=0)
    network = find_network(data)
    G = setup_graph(data)
    print(compute_in_citations(network, G))
    


def find_network(data):
    '''This function finds a network based on some criteria

    Args:
        graph (DiGraph)
    '''
    return data.to.unique()

def compute_in_citations(network, graph):
    '''Computes metric of inwardness according to the equation
    inwardness = (self-citations) / (total citations) * 100

    Args:
        network (list of obj): ids in the network
        graph (DiGraph): graph of the network
    
    Returns:
        inwardness measure (float)
    '''
    self_citations = 0
    total_citations = 0

    # for papers in network (whatever that is)
    for paper in network:
        # find iterator for all citations of (ie: this id in 2 column)
        cites = graph.predecessors(paper)
        
        while True:
            try:
                citation = next(cites)
                # if paper is also in network iterate self citations
                if citation in network:
                    self_citations += 1
                # also iterate total citations
                total_citations += 1
            except StopIteration:
                break
    if total_citations == 0:
        inwardness = 0
    else:
        inwardness = self_citations / total_citations * 100

    print(self_citations)
    print(total_citations)

    return inwardness


# Graph creation setup
def setup_graph(data):
    '''Sets up a graph network

    Args:
        data (dataframe of all data)
    
    Returns:
        a graph
    '''
    
    G = nx.DiGraph()

    # Put into graph format
    for row in data.index:
        connection = (data['from'][row], data['to'][row])
        G.add_nodes_from(connection)
        G.add_edge(*connection)

    return G


