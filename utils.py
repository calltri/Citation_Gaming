import pandas as pd
from neo4j import GraphDatabase
import networkx as nx
import tqdm
import pdb
import os
import sys,os
import seaborn as sns
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join("journal-citation-cartels/libs/cidre")))
from cidre import cidre, filters
from cidre import cidre, filters, draw
import numpy as np

def evaluate_network():
    fileName = os.path.join("input_data", "criminology_citations.csv")
    data = pd.read_csv(fileName, header=0)
    network = find_network(data)
    G = setup_graph(data)
    print(call_cidre(G))

    #print(compute_in_citations(network, G))
    


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



def call_cidre(graph, theta = 0.15):
    '''Calls cidre on a given graph

    Args:
        network (list of membership for all groups, 0=none)
        graph (DiGraph)
    '''
    # Generate network
    net = nx.karate_club_graph()
    W = nx.adjacency_matrix(net)
    print("W:")
    print(W[:20])
    # Count of citations between two nodes
    W.data = np.random.poisson(10, W.data.size)

    # Doing some random stuff for scholastic method!!!!!
    W_threshold = W.copy()
    W_threshold.data = np.random.poisson(15, W_threshold.data.size)
    #import pdb; pdb.set_trace()

    # Generate random community memberships
    community_ids = np.random.choice(2, W.shape[0], replace=True).astype(int)

    print("W:")
    print(W[:20])
    print("Threshold:")
    print(W_threshold[:20])
    print("comunity id:")
    print(community_ids[50:])

    is_excessive_func = filters.get_dcsbm_threshold_filter(
        W, W_threshold, community_ids
    )

    # Detect the cartel groups
    citation_group_table = cidre.detect(W, theta, is_excessive_func)

    # Load the class for drawing a cartel
    dc = draw.DrawCartel()

    # Set up the canvas
    fig, axes = plt.subplots(figsize=(10,10))
    sns.set_style("white")
    sns.set(font_scale = 1.2)
    sns.set_style("ticks")

    # Set the name of each node
    citation_group_table["name"] = citation_group_table["node_id"].apply(lambda x : str(x))

    for cid, cartel in citation_group_table.groupby("group_id"):
        dc.draw(
            W,
            cartel.node_id.values.tolist(),
            cartel.donor_score.values.tolist(),
            cartel.recipient_score.values.tolist(),
            theta,
            cartel.name.values.tolist(),
            ax=axes,
        )
        plt.show()

    return citation_group_table

    '''
    How it works:
    In construct_network downloads + compiles data into frames
    No idea how weights work into this - but crashes without them?
    lots of pickling to compute the data
    '''

