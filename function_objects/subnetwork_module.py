# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 12:57:21 2020

@author: jwKim
"""
import numpy as np

from ..data_objects import Network_objects

def make_subgraph_unsigned_graph_using_indexes(unsigned_graph, l_indexes_subgraph):
    unsigned_graph_sub = Network_objects.Unsigned_graph(str(unsigned_graph)+"_sub")
    l_nodenames_sub = [unsigned_graph.show_nodenames()[i] for i in l_indexes_subgraph]
    unsigned_graph_sub.set_nodenames(l_nodenames_sub)
    
    unsigned_graph_sub.set_unsigned_graph_matrix(unsigned_graph.show_unsigned_graph_matrix_form()[np.ix_(l_indexes_subgraph,l_indexes_subgraph)])
    
    return unsigned_graph_sub

def make_subgraph_unsigned_graph(unsigned_graph, l_s_nodes_subgraph):
    l_indexes_subgraph = [unsigned_graph.show_nodenames().index(s_node) for s_node 
                          in l_s_nodes_subgraph]
    return make_subgraph_unsigned_graph_using_indexes(unsigned_graph, l_indexes_subgraph)