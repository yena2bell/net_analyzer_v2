# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 10:46:28 2020

@author: jwKim
"""
import numpy as np

def is_connected_graph(graph):#unsigned graph
    matrix_unsigned_graph = graph.show_unsigned_graph_matrix_form()
    return is_connected_directed_matrix(matrix_unsigned_graph)

def is_connected_directed_matrix(matrix_directed_unsigned):
    if len(matrix_directed_unsigned) == 1:
        return True
    matrix_undirected_selploop = matrix_directed_unsigned + np.identity(len(matrix_directed_unsigned)) + np.transpose(matrix_directed_unsigned)
    matrix_power = matrix_undirected_selploop
    for _ in range(len(matrix_directed_unsigned)-1):
        if matrix_power[0].all():
            return True
        matrix_power = np.matmul(matrix_power, matrix_undirected_selploop)
    return False


def show_connected_components(graph):#unsigned graph
    l_l_components = []
    l_checked_index = []
    matrix_unsigned_graph = graph.show_unsigned_graph_matrix_form()
    matrix_undirected_selploop = matrix_unsigned_graph + np.identity(len(graph)) + np.transpose(matrix_unsigned_graph)
    matrix_power = matrix_undirected_selploop
    for _ in range(len(graph)-1):
        matrix_power = np.matmul(matrix_power, matrix_undirected_selploop)
        
    i_index = 0
    while i_index < len(graph):
        if i_index in l_checked_index:
            continue
        new_component = list(np.nonzero(matrix_power[i_index])[0])
        l_l_components.append(new_component)
        l_checked_index.extend(new_component)