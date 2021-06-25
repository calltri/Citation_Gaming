import pandas as pd
from neo4j import GraphDatabase
import networkx as nx
import tqdm
import pdb
import utils

def query_paper_doi_from(tx, dois):
    return tx.run('''
        MATCH (p1:papers)-[r:PaperReferences]->(p2:papers)
        WHERE  p1.Doi IN $dois
        RETURN p1.PaperId, p2.PaperId
        ''', dois=dois).values()

def query_paper_doi_to(tx, dois):
    return tx.run('''
        MATCH (p1:papers)<-[r:PaperReferences]-(p2:papers)
        WHERE p1.Doi IN $dois
        RETURN p1.PaperId, p2.PaperId
        ''', dois=dois).values()

def query_paper_id_from(tx, ids):
    return tx.run('''
        MATCH (p1:papers)-[r:PaperReferences]->(p2:papers)
        WHERE  p1.PaperId IN $ids
        RETURN p1.PaperId, p2.PaperId
        ''', ids=ids).values()

def query_paper_id_to(tx, ids):
    return tx.run('''
        MATCH (p1:papers)<-[r:PaperReferences]-(p2:papers)
        WHERE  p1.PaperId IN $ids
        RETURN p1.PaperId, p2.PaperId
        ''', ids=ids).values()

def compute_basic_citation_graph():
    df = pd.read_csv('SCORE_csv.csv')
    dois = [x.upper() for x in df['DOI_CR']]

    driver = GraphDatabase.driver("bolt://minds04.isi.edu:7687", auth=('neo4j', 'mag'))
    paper_graph = set()
    G = nx.DiGraph()

    with driver.session() as session:
        #direct cited papers
        results = session.read_transaction(query_paper_doi_from, dois)
        for r in results:
            G.add_nodes_from(r)
            G.add_edge(*r)

        results = session.read_transaction(query_paper_doi_to, dois)
        for r in results:
            G.add_nodes_from(r)
            G.add_edge(*r)

        #indirect cited papers
        #comment out because they are very slow
        '''
        N_QUERY_SIZE = 100
        for hop in range(1):
            print('Hop', hop)
            paper_ids = list(G.nodes().keys())
            for i in tqdm.tqdm(range(0, len(paper_ids), N_QUERY_SIZE)):
                ids = paper_ids[i:i+N_QUERY_SIZE]
                results = session.read_transaction(query_paper_id_from, ids)
                for r in results:
                    G.add_nodes_from(r)
                    G.add_edge(*r)

                results = session.read_transaction(query_paper_id_to, ids)
                for r in results:
                    G.add_nodes_from(r)
                    G.add_edge(*r)
        '''

    print('#nodes', G.number_of_nodes())
    print('#edges', G.number_of_edges())

    ranks = nx.algorithms.link_analysis.pagerank_alg.pagerank_scipy(G)
    ranks_list = list(ranks.items())
    ranks_list.sort(key=lambda x: x[1])
    print(f'Min Score: {ranks_list[0][1]}, @PaperId {ranks_list[0][0]}',)
    print(f'Max Score: {ranks_list[-1][1]}, @PaperId {ranks_list[-1][0]}',)

    # No real way to connect the graph to the dataset
    # Explore Neo4j and see if that has answers

if __name__ == '__main__':
    utils.evaluate_network()