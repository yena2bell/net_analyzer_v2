# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 11:14:24 2020

@author: jwKim
"""
import numpy as np

#use Kosaraju’s algorithm
#https://www.geeksforgeeks.org/strongly-connected-components/
#time complexity is O(V+E)
def decompose_to_SCC_unsigned_graph(graph):#for unsigned graph
    l_l_SCC = decompose_to_SCC(graph.show_unsigned_graph_matrix_form())
    l_l_s_SCC = []
    for l_SCC in l_l_SCC:
        l_l_s_SCC.append([graph.show_nodenames()[i] for i in l_SCC])
    
    return l_l_s_SCC


def decompose_to_SCC(matrix):
    l_l_SCC = []
    l_node_flow = SCC_algorithm_Kosaraju_stack_calculation(matrix)
    
    array_visited = np.zeros(len(matrix),dtype=bool)
    
    matrix_transpose = np.transpose(matrix.copy())
    
    while l_node_flow:
        i_index = l_node_flow.pop()
        l_SCC = []
        if not array_visited[i_index]:
            l_l_SCC.append(_DFSUtil(i_index, array_visited, 
                                    matrix_transpose, l_SCC))
    
    return l_l_SCC

def is_SCC_unsigned_graph(graph):
    return is_SCC(graph.show_unsigned_graph_matrix_form())
            
def is_SCC(matrix):
    l_node_flow = SCC_algorithm_Kosaraju_stack_calculation(matrix)
    
    array_visited = np.zeros(len(matrix),dtype=bool)
    
    matrix_transpose = np.transpose(matrix.copy())
    while l_node_flow:
        i_index = l_node_flow.pop()
        l_SCC=[]
        if not array_visited[i_index]:
            l_SCC = _DFSUtil(i_index, array_visited, 
                             matrix_transpose, l_SCC)
            if len(l_SCC) < len(matrix):
                return False
            else:
                return True

def SCC_algorithm_Kosaraju_stack_calculation(matrix):
    l_node_flow = []
    matrix_directed = matrix.copy()
    array_visited = np.zeros(len(matrix),dtype=bool)
    
    for i_index in range(len(matrix)):
        if not array_visited[i_index]:
            _fill_order(i_index, array_visited, 
                        l_node_flow, matrix_directed)
    
    return l_node_flow#at least one node of the upper hierarchy SCC is located latter in the l_node_flow than the lower hierarchy SCC
            
def _DFSUtil(i_index, array_visited, matrix_transpose, l_SCC):
    array_visited[i_index] = True
    l_SCC.append(i_index)
    for i_downstream in np.nonzero(matrix_transpose[:, i_index])[0]:
        if not array_visited[i_downstream]:
            l_SCC = _DFSUtil(i_downstream, array_visited, 
                                  matrix_transpose, l_SCC)
    return l_SCC
            
            
def _fill_order(i_index, array_visited, l_node_flow, matrix_directed):
    array_visited[i_index] = True
    for i_downstream in np.nonzero(matrix_directed[:,i_index])[0]:
        if not array_visited[i_downstream]:
            _fill_order(i_downstream, array_visited, 
                        l_node_flow, matrix_directed)
    l_node_flow.append(i_index)