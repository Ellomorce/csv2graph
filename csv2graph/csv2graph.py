import pandas as pd
import glob
import os
import networkx as nx
import itertools
import csv
import pydot
from IPython.display import Image
#
def make_graph(nodes, edges):
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G
#
def make_edges(node_list, label_dict):
    with open('number_logic.csv', newline='') as f:
        reader = csv.reader(f)
        number_logic = [tuple(map(int, row)) for row in reader]
    edge_raw = [i for i in itertools.combinations(node_list, 2)]
    edge1 = [j for j in edge_raw if j in number_logic]
    df_e = pd.DataFrame(edge1, columns = ['f_node', 'b_node'])
    df_e['label'] = df_e['b_node'].map(label_dict)
    edge2 = [[*i, j] for i,j in zip(list(df_e[['f_node', 'b_node']].itertuples(index=False, name=None)), 
                                    df_e.drop(['f_node', 'b_node'], axis='columns').to_dict('records'))] 
    edges = [tuple(l) for l in edge2]
    return edges
#
def networkx2dot(G):
    strict = nx.number_of_selfloops(G) == 0 and not G.is_multigraph()
    GDOT = pydot.Dot("OKRMAP", graph_type="digraph", strict=strict, resolution='300.0', size="15,15!", fontname='Microsoft JhengHei') #rankdir="LR"
    GDOT.graph_defaults = G.graph.get("graph", {})
    GDOT.set_node_defaults(shape='box', style="filled", color="black", fillcolor="white", fontname='Microsoft JhengHei')
    GDOT.set_edge_defaults(fontname='Microsoft JhengHei', labelfontsize='10.0')
    
    for n, nodedata in G.nodes(data=True):
        if n !=None:
            node_lst = list(nodedata.values())
            node_dict = str(node_lst[0])
            node_label = str(n)+'\n'+node_dict
            dotnode = pydot.Node(n, label = node_label)
            GDOT.add_node(dotnode)

    for u, y, edgedata in G.edges(data=True):
        if y !=None:
            edge_lst = list(edgedata.values())
            edge_label = str(edge_lst[0])
            dotedge = pydot.Edge(str(u), str(y), label = edge_label)
            GDOT.add_edge(dotedge)
    return GDOT
#
path = "okrlist"
csv_files = glob.glob(os.path.join(path, "*.csv"))
for filename in csv_files:
    df = pd.read_csv(filename, usecols = ['Number','Title', 'statement'], encoding='utf8')
    df2 = df.drop(['Number','statement'], axis='columns')
    df3 = df.drop(['Title'], axis='columns')
    node_list = list(df['Number'])
    node_label = df2.to_dict('records')
    nodes = list(zip(node_list, node_label))
    label_dict = dict(zip(df3['Number'], df3['statement']))
    edges = make_edges(node_list, label_dict)
    G = make_graph(nodes, edges)
    GDOT = networkx2dot(G)
    GDOT.write_png('{}.png'.format(filename), encoding='utf8')