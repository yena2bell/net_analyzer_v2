# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 17:28:38 2020

@author: jwKim
"""
import numpy as np
from collections import defaultdict

from . import SCC_module

def find_cycles_unsigned_graph(unsigned_graph):
    object_cycles_finder = Find_cycles(unsigned_graph.show_unsigned_graph_matrix_form())
    object_cycles_finder.find_cycles()
    l_l_i_cycles = object_cycles_finder.show_all_cycles()
    
    l_l_s_cycles = []
    l_s_nodenames = unsigned_graph.show_nodenames()
    for l_i_cycles in l_l_i_cycles:
        l_s_cycles = [l_s_nodenames[i] for i in l_i_cycles]
        l_l_s_cycles.append(l_s_cycles)
    
    return l_l_s_cycles

class Find_cycles:
    #Johnson's algorithm
    def __init__(self, matrix_unsigned):
        self.matrix_unsigned = np.matrix(matrix_unsigned)
        self.i_num_of_nodes = len(self.matrix_unsigned)
        self.l_l_SCCs = []
        self._decompose_SCC()
        self.l_l_i_cycles = []
    
    def _decompose_SCC(self):
        self.l_l_SCCs = SCC_module.decompose_to_SCC(self.matrix_unsigned)
    
    def _modify_cycles(self, l_l_i_cycles, l_SCC):
        l_l_i_cycles_modified = []
        for l_i_cycle in l_l_i_cycles:
            l_i_cycle_modified = [l_SCC[i] for i in l_i_cycle]
            l_l_i_cycles_modified.append(l_i_cycle_modified)

        return l_l_i_cycles_modified
    
    def _make_cycles_finder_object_of_SCC(self, l_SCC):
        matrix_unsigned_of_SCC = np.matrix(self.matrix_unsigned[np.ix_(l_SCC,l_SCC)])
        object_cycles_finder = Find_cycles_in_SCC(matrix_unsigned_of_SCC)
        
        return object_cycles_finder
        
    def _find_cycles_in_SCC(self, l_SCC):
        object_cycles_finder = self._make_cycles_finder_object_of_SCC(l_SCC)
        l_l_i_cycles = object_cycles_finder.find_cycles()
        
        return self._modify_cycles(l_l_i_cycles, l_SCC)
    
    def find_cycles(self):
        for l_SCC in self.l_l_SCCs:
            l_l_i_cycles = self._find_cycles_in_SCC(l_SCC)
            self.l_l_i_cycles.extend(l_l_i_cycles)
    
    def show_all_cycles(self):
        return self.l_l_i_cycles
        

class Find_cycles_in_SCC:
    def __init__(self, unsigned_matrix):
        self.matrix_unsigned = np.matrix(unsigned_matrix)
        self.i_num_of_nodes = len(self.matrix_unsigned)
        self.l_l_i_cycles = []
        
    def _modify_cycles(self, l_l_i_cycles, i_0_of_new_matrix):
        l_l_i_cycles_modified = []
        for l_i_cycle in l_l_i_cycles:
            l_i_cycle_modified = [i+i_0_of_new_matrix for i in l_i_cycle]
            l_l_i_cycles_modified.append(l_i_cycle_modified)

        return l_l_i_cycles_modified
        
    def _find_cycles_on_node_over_i(self, i_0_of_new_matrix):
        matrix_over_node_i = np.matrix(self.matrix_unsigned[i_0_of_new_matrix:,i_0_of_new_matrix:])
        object_cycle_finder = Find_cycles_containing_0(matrix_over_node_i)
        l_l_i_cycles = object_cycle_finder.find_cycles()

        return self._modify_cycles(l_l_i_cycles, i_0_of_new_matrix)
    
    def find_cycles(self):
        for i in range(self.i_num_of_nodes):
            self.l_l_i_cycles.extend(self._find_cycles_on_node_over_i(i))
        
        return self.l_l_i_cycles
    

class Find_cycles_containing_0:
    def __init__(self, matrix_unsigned):
        self.matrix_unsigned = np.matrix(matrix_unsigned)
        self.i_num_of_nodes = len(matrix_unsigned)
        
        self.dic_i_start_array_ends = {}
        self.dic_i_start_i_count = {}
        self.dic_i_start_i_count_saved = {}
        self._refine_topology_information()
        
        self.l_l_i_cycles = []
        
        self.array_blocked = np.zeros((self.i_num_of_nodes,), dtype=bool)
        self.l_flow = []
        self.l_connectable_to_0 = []#has same length to l_flow. if l_connectable_to_0[i] = True: l_flow[:i+1] can reach to 0(root node)
        self.dic_blocked_link = defaultdict(set)#if dic_blocked_link[i] contains j, then j->i link is blocked
        
    def _refine_topology_information(self):
        for i_node in range(self.i_num_of_nodes):
            array_ends = np.nonzero(self.matrix_unsigned[:,i_node])[0]
            self.dic_i_start_array_ends[i_node] = array_ends
            self.dic_i_start_i_count[i_node] = len(array_ends)-1
            self.dic_i_start_i_count_saved[i_node] = self.dic_i_start_i_count[i_node]
        
    def _unblock(self, i_node):
        if self.array_blocked[i_node]:#i is blocked:
            self.array_blocked[i_node] = False #reset of blocking
        if self.dic_blocked_link[i_node]:#dic_blocked_link[i_node] is set
            for i_node_start in list(self.dic_blocked_link[i_node]):#i_node_start->i_node links are blocked
                self.dic_blocked_link[i_node].discard(i_node_start)# reset i_node_start->i_node links
                self._unblock(i_node_start)
    
    def _extend_flow(self, i_node):
        self.l_flow.append(i_node)
        self.l_connectable_to_0.append(False)
        self.array_blocked[i_node] = True
        
    def _block_links(self, i_node):
        for i_node_end in self.dic_i_start_array_ends[i_node]:
            self.dic_blocked_link[i_node_end].add(i_node)
    
    def _passable_case(self, i_next_edge):
        i_node_next = self.dic_i_start_array_ends[self.l_flow[-1]][i_next_edge]
        self.dic_i_start_i_count[self.l_flow[-1]] -= 1
        if i_node_next == 0:#it is a cycle containing 0
            self.l_connectable_to_0[-1] = True#l_flow[-1] node is connected to 0 node
            self.l_l_i_cycles.append(self.l_flow.copy())
        elif not self.array_blocked[i_node_next]:# not passed this node yet
            self._extend_flow(i_node_next)
    
    def _impassble_case(self):
        i_end = self.l_flow.pop(-1)
        b_end = self.l_connectable_to_0.pop(-1)
        if self.l_flow:
            self.dic_i_start_i_count[i_end] = self.dic_i_start_i_count_saved[i_end]#reset the passage of links starting from this node
            if b_end:
                self._unblock(i_end)
                self.l_connectable_to_0[-1] = True
            else:
                self._block_links(i_end)
        
        
    def find_cycles(self):
        if self.i_num_of_nodes == 1:
            if self.matrix_unsigned[0,0] >= 1:#self loop
                self.l_l_i_cycles.append([0])
        else:
            self._extend_flow(0)
            while self.l_flow:
                i_next_edge = self.dic_i_start_i_count[self.l_flow[-1]]
                if i_next_edge >=0:
                    self._passable_case(i_next_edge)
                else:
                    self._impassble_case()
                
        return self.l_l_i_cycles
