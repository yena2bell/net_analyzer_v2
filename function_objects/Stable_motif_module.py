# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 13:21:48 2020

@author: jwKim
"""
import numpy as np
import multiprocessing
import time

from .Topology_functions import SCC_module
from .Topology_functions import Connectedness_module
from .Topology_functions import Cycles_module
from . import Iterator_module
from . import Converter_module
from . import Multiprocessing_tools


def find_stable_motifs(unsigned_graph, 
                       expanded_network, 
                       i_min=1, i_max=None, 
                       l_dict_stable_motifs_known=[], 
                       s_address_results=None,
                       i_num_process=1):
    
    l_l_SCC = SCC_module.decompose_to_SCC(unsigned_graph.show_unsigned_graph_matrix_form())
    
    if i_max == None:
        i_max = len(unsigned_graph)
    for i_num_of_nodes in range(i_min, i_max+1):
        
        print(i_num_of_nodes," nodes stable motif calculation starts")
        if s_address_results:
            with open(s_address_results, 'a') as file_results:
                file_results.write(str(i_num_of_nodes))
                file_results.write(" nodes stable motif calculation starts\n")
        
        f_time = time.time()
        l_l_dict_stable_motifs_news = []
        for l_SCC in l_l_SCC:
            if len(l_SCC) >= i_num_of_nodes:
                if i_num_process == 1:
                    l_dict_stable_motifs_new = find_stable_motif_given_num_of_nodes(unsigned_graph, expanded_network, l_SCC, i_num_of_nodes, l_dict_stable_motifs_known, s_address_results)
                else:                    
                    l_dict_stable_motifs_new = find_stable_motif_given_num_of_nodes_mulitprocess(unsigned_graph, expanded_network, l_SCC, i_num_of_nodes, i_num_process, l_dict_stable_motifs_known, s_address_results)
                l_l_dict_stable_motifs_news.append(l_dict_stable_motifs_new)
        for l_dict_stable_motifs_new2 in l_l_dict_stable_motifs_news:
            l_dict_stable_motifs_known.extend(l_dict_stable_motifs_new2)
            
        print(i_num_of_nodes," nodes stable motif calculation ended. it takes ", time.time()-f_time, " seconds")
        if s_address_results:
            with open(s_address_results, 'a') as file_results:
                file_results.write(str(i_num_of_nodes))
                file_results.write(" nodes stable motif calculation ended. it takes ")
                file_results.write(str(time.time()-f_time))
                file_results.write(" seconds\n")
    
    return l_dict_stable_motifs_known

def find_stable_motif_given_num_of_nodes(unsigned_graph, 
                                         expanded_network,
                                         l_SCC,
                                         i_num_of_nodes, 
                                         l_dict_stable_motifs_known=[], s_address_results=None):
    l_dict_stable_motifs = []
    
    iterator_given = Iterator_module.generator_combination_num_in_defined_1(len(l_SCC), i_num_of_nodes)
    l_dict_stable_motifs.extend(find_stable_motif_given_comb_iterator(unsigned_graph,
                                                                      expanded_network,
                                                                      iterator_given,
                                                                      l_SCC,
                                                                      l_dict_stable_motifs_known,
                                                                      s_address_results,
                                                                      1,0))
    return l_dict_stable_motifs

def find_stable_motif_given_num_of_nodes_mulitprocess(unsigned_graph, expanded_network, l_SCC, i_num_of_nodes, i_num_process=1, l_dict_stable_motifs_known=[], s_address_results=None):
    l_dict_stable_motifs_new = []
    l_procs = []
    queue_to_use = multiprocessing.Queue()
    for i in range(i_num_process):
        l_argument = []
        l_argument.append(unsigned_graph)
        l_argument.append(expanded_network)
        l_argument.append(l_SCC)
        l_argument.append(i_num_of_nodes)
        l_argument.append(l_dict_stable_motifs_known)
        l_argument.append(s_address_results)
        l_argument.append(i_num_process)
        l_argument.append(i)
        l_argument.append(queue_to_use)
        
        l_procs.append(multiprocessing.Process(target=_find_stable_motif_in_multiprocess, args=(l_argument,)))
    
    for proc in l_procs:
        proc.start()
    
    array_not_yet_ended = np.zeros((i_num_process,), dtype=bool)
    while not array_not_yet_ended.all():
        data = queue_to_use.get()
        if type(data) == type([]):
            l_dict_stable_motifs_new.extend(data)
        elif (type(data) == type((1,))) and data[0] == "finish":
            array_not_yet_ended[data[1]] = True
            print(data[1],"'th process finished")
    queue_to_use.close()
    queue_to_use.join_thread()
    
    for proc in l_procs:
        proc.join()
    
    return l_dict_stable_motifs_known+l_dict_stable_motifs_new
        
def _find_stable_motif_in_multiprocess(l_arguments):
    unsigned_graph = l_arguments[0]
    expanded_network = l_arguments[1]
    l_SCC = l_arguments[2]
    i_num_of_nodes = l_arguments[3]
    l_dict_stable_motifs_known = l_arguments[4]
    s_address_results = l_arguments[5]
    i_num_all_processes = l_arguments[6]
    i_index_process = l_arguments[7]
    queue_results_sender = l_arguments[8]
    
    iterator_of_this_process = Iterator_module.generator_combination_num_in_defined_1(len(l_SCC), 
                                                                                      i_num_of_nodes, 
                                                                                      i_num_all_processes, 
                                                                                      i_index_process)
    l_dict_stable_motifs = find_stable_motif_given_comb_iterator(unsigned_graph,
                                                                 expanded_network,
                                                                 iterator_of_this_process,
                                                                 l_SCC,
                                                                 l_dict_stable_motifs_known,
                                                                 s_address_results,
                                                                 i_num_all_processes,
                                                                 i_index_process)
    
    _send_result_and_end_message_semaphore = Multiprocessing_tools.decorator_semaphore_using_time(i_index_process, i_num_all_processes, 1, _send_result_and_end_message)
    _send_result_and_end_message_semaphore(queue_results_sender, l_dict_stable_motifs, i_index_process)
    
    
def _send_result_and_end_message(queue_to_use, l_results, i_index_process):
    queue_to_use.put(l_results)
    queue_to_use.put(("finish", i_index_process))
    
    
        
def find_stable_motif_given_comb_iterator(unsigned_graph, 
                                          expanded_network, 
                                          iterator_given,
                                          l_i_comb_to_indexes,
                                          l_dict_stable_motifs_known=[], 
                                          s_address_results=None, 
                                          i_num_processes = 1, 
                                          i_index_process=0):
    write_stable_motifs_semaphore = Multiprocessing_tools.decorator_semaphore_using_time(i_index_process, i_num_processes, 1, write_stable_motifs)
    l_dict_stable_motifs_new = []
    array_i_comb_to_indexes = np.array(l_i_comb_to_indexes)
#    i_count = 0
#    tmp_fun_sema= Multiprocessing_tools.decorator_semaphore_using_time(i_index_process, i_num_processes, 1, tmp_fun)
    for i_comb in iterator_given:
#        i_count+=1
        array_index_nodes = array_i_comb_to_indexes[Converter_module.int_to_arraystate_bool(i_comb, len(array_i_comb_to_indexes))]
        l_dict_stable_motifs_in_comb = find_stable_motif_given_nodes(unsigned_graph, expanded_network, array_index_nodes, l_dict_stable_motifs_known)
        if l_dict_stable_motifs_in_comb:
            if s_address_results:
                write_stable_motifs_semaphore(s_address_results, l_dict_stable_motifs_in_comb, unsigned_graph)
        l_dict_stable_motifs_new.extend(l_dict_stable_motifs_in_comb)
#    tmp_fun_sema(s_address_results, str(i_index_process)+" cal "+str(i_count))
    return l_dict_stable_motifs_new
        
#def tmp_fun(s_address_to_write, s_message):
#    with open(s_address_to_write, 'a') as file_results:
#        file_results.write(s_message)

def write_stable_motifs(s_address_to_write, l_dict_stable_motifs, unsigned_graph):
    with open(s_address_to_write, 'a') as file_results:
        for dict_stable_motif in l_dict_stable_motifs:
            file_results.write(str(len(dict_stable_motif))+" nodes stable motif: ")
            for i_index_node, i_state in dict_stable_motif.items():
                file_results.write(str(unsigned_graph.show_nodenames()[i_index_node]))
                file_results.write("=")
                file_results.write(str(int(i_state)))
                file_results.write(" ")
            file_results.write('\n')


def find_stable_motif_given_nodes(unsigned_graph, expanded_network, l_index_nodes, l_dict_stable_motifs_known=[]):
    l_dict_stable_motifs = []
    if not _check_stable_motif_condition1(unsigned_graph, l_index_nodes):
        return []
    else:
        l_t_arrays_known_stable_motifs_info = _avoid_known_stable_motifs(l_dict_stable_motifs_known, l_index_nodes)
        #l_t_arrays_known_stable_motifs_info = [(array1, array2)] array2 have stable motifs nodes information.
        #array1[array2] becomes the state of the known stable motif
        #if (array_state == t_arrays[0])[t_arrays[1]].all(), then array_state contains state of stable motif
        for array_state in Iterator_module.iterator_all_state(len(l_index_nodes),{},1,0):
            for t_arrays in l_t_arrays_known_stable_motifs_info:
                if (array_state == t_arrays[0])[t_arrays[1]].all():
                    break
            else:
                if _check_stable_motif_condition2(expanded_network, l_index_nodes ,array_state):
                    l_dict_stable_motifs.append(dict(zip(l_index_nodes, array_state)))
        
    return l_dict_stable_motifs

def _avoid_known_stable_motifs(l_dict_stable_motifs_known, l_index_nodes):
    l_t_arrays_known_stable_motifs_info = []
    l_index_nodes = list(l_index_nodes)
    for dict_stable_motifs_known in l_dict_stable_motifs_known:
        if len(dict_stable_motifs_known) <= len(l_index_nodes):
            if set(dict_stable_motifs_known.keys()).issubset(set(l_index_nodes)):
                array_form = np.zeros((len(l_index_nodes),))
                l_positions_to_check = []
                for i_index, state in dict_stable_motifs_known.items():
                    array_form[l_index_nodes.index(i_index)] = state
                    l_positions_to_check.append(l_index_nodes.index(i_index))
                l_t_arrays_known_stable_motifs_info.append((array_form, np.array(l_positions_to_check)))
    
    return l_t_arrays_known_stable_motifs_info
                
            

def _check_stable_motif_condition1(unsigned_graph, l_indexes_nodes_in_graph):
    matrix_sub = unsigned_graph.show_unsigned_graph_matrix_form()[np.ix_(l_indexes_nodes_in_graph,l_indexes_nodes_in_graph)]
    if not Connectedness_module.is_connected_directed_matrix(matrix_sub):
        return False
    if not SCC_module.is_SCC(matrix_sub):
        return False
    return True
    

def _check_stable_motif_condition2(expanded_network, l_indexes_nodes_in_graph ,array_state):
    #check whether the motif is stable using expanded network.
    l_indexes_single_nodes = [l_indexes_nodes_in_graph[i]*2 + array_state[i] for i in range(len(l_indexes_nodes_in_graph))]
    #off nodes are in even index, and on nodes are on odd indexes
    #array state is 0 if off state, 1 if on state
    if _check_stable_motif_using_expanded_network_using_indexes(expanded_network, l_indexes_single_nodes):
        return True
    else:
        return False
    

def _check_stable_motif_using_expanded_network_using_indexes(expanded_network, l_indexes_single_nodes):
    #l_indexes_single_nodes should has indexes of single nodes
    l_indexes_composite_nodes = []
    set_indexes_single_nodes = set(l_indexes_single_nodes)
    
    for i_index_single in l_indexes_single_nodes:
        array_index_composite = _find_index_composite_regulators(expanded_network, i_index_single)#regulator composite nodes of the single node
        l_i_composites = [i_index_composite for i_index_composite 
                          in array_index_composite 
                          if _check_i_composite_node(expanded_network, 
                                                     i_index_composite, 
                                                     set_indexes_single_nodes)]#composite nodes whose regulators are all in l_indexes_single_nodes
        l_indexes_composite_nodes.extend(l_i_composites)
    
    matrix_sub = expanded_network.show_unsigned_graph_matrix_form()[np.ix_(l_indexes_single_nodes+l_indexes_composite_nodes, l_indexes_single_nodes+l_indexes_composite_nodes)]
    if len(matrix_sub) == 1:
        return matrix_sub[0,0] >=1#exception! only when 1 node stable motif calculation.
    else:
        return SCC_module.is_SCC(matrix_sub)
#        if SCC_module.is_SCC(matrix_sub):
#            print([expanded_network.show_nodenames()[i] for i in l_indexes_single_nodes])
#            print(l_indexes_single_nodes)
#            print([expanded_network.show_nodenames()[i] for i in l_indexes_composite_nodes])
#            print(l_indexes_composite_nodes)
#            print(expanded_network.show_unsigned_graph_matrix_form())
#            print(matrix_sub)
#            return True
#        else:
#            return False
        
        
def _find_index_composite_regulators(expanded_network, i_index_single):
    #find_index of composite_regulators of the single_node given index form.
    array_regulators = expanded_network.show_indexes_of_regulators_of_node(i_index_single)
    return array_regulators[array_regulators>=len(expanded_network.show_single_nodenames())]

def _check_i_composite_node(expanded_network, i_composite_node, set_index_single_nodes):
    #check whether the composite node's regulators are all included in the given single nodes
    return set(expanded_network.show_indexes_of_regulators_of_node(i_composite_node)).issubset(set_index_single_nodes)


def find_stable_motifs_using_expanded_net_cycles(expanded_network):
    object_expanded_net_cycle_finder = Find_cycles_in_expaned_net_for_stable_motifs(expanded_network)
    object_expanded_net_cycle_finder.find_cycles()
    return object_expanded_net_cycle_finder.show_cycles_only_single_nodes(), object_expanded_net_cycle_finder.show_cycles_containing_composite_node()

class Find_cycles_in_expaned_net_for_stable_motifs(Cycles_module.Find_cycles):
    def __init__(self, expanded_network):
        self.expanded_network = expanded_network
        Cycles_module.Find_cycles.__init__(self, expanded_network.show_unsigned_graph_matrix_form())
        self.dict_i_node_array_contradicted_nodes = {}
        #{i:array(i2,i3,i4)} i_th expanded node can't be with i2,i3,i4 th expanded node in this cycle. 
        #if i_th node is A_on, then node containing A_off becomes i2,i3,i4 th nodes.
        #if i_th node is A_on__AND__B_off, A_off and B_on becomes value of key i
        self._make_dict_of_opposing_state_containing_nodes()
        
        self.l_l_i_cycles_containing_composite = []
        self.l_l_i_cycles_only_single = []
        
    def _decompose_SCC(self):# let the single node indexes are behind of composite node indexes
        Cycles_module.Find_cycles._decompose_SCC(self)
        for l_SCC in self.l_l_SCCs:
            l_SCC.sort(reverse=True)
    
    def _make_dict_of_opposing_state_containing_nodes(self):
        #make self.dict_i_node_array_contradicted_nodes
        for i in range(len(self.expanded_network.show_single_nodenames())):
            i_index_opposite_state = self.expanded_network.show_index_of_inverse_state_of_node(i)
            self.dict_i_node_array_contradicted_nodes[i] = np.concatenate(([i_index_opposite_state], self.expanded_network.show_indexes_of_composite_node_containing_single_node(i_index_opposite_state)))
        for i in range(len(self.expanded_network.show_composite_nodenames())):
            i_index = i+ len(self.expanded_network.show_single_nodenames())
            self.dict_i_node_array_contradicted_nodes[i_index] = np.array([self.expanded_network.show_index_of_inverse_state_of_node(i_simple_node) for i_simple_node in self.expanded_network.show_indexes_of_regulators_of_node(i_index)])
    
    def _find_conditions_to_SCC(self, l_SCC):
        dict_i_node_array_contradictend_nodes_in_SCC = {}
        for i in range(len(l_SCC)):
            i_index_in_all = l_SCC[i]
            array_contradicts = self.dict_i_node_array_contradicted_nodes[i_index_in_all]
            l_tmp = []
            for i_contradict in array_contradicts:
                if i_contradict in l_SCC:
                    l_tmp.append(l_SCC.index(i_contradict))
            dict_i_node_array_contradictend_nodes_in_SCC[i] = np.array(l_tmp)
        
        return dict_i_node_array_contradictend_nodes_in_SCC
    
    def _find_position_single_node_start(self, l_indexes):
        #l_indexes are sorted reversely. so bigger indexes comes earlier.
        #so composite nodes are all in front part
        #return position of the first coming single node index
        for i, i_index in enumerate(l_indexes):
            if i_index < len(self.expanded_network.show_single_nodenames()):
                return i
            
        raise ValueError(str(l_indexes)+" has no single node index!")  
    
    def _find_cycles_in_SCC(self, l_SCC):
        matrix_unsigned_of_SCC = np.matrix(self.matrix_unsigned[np.ix_(l_SCC,l_SCC)])
        dict_i_node_array_contradicts_SCC = self._find_conditions_to_SCC(l_SCC)
        i_position_of_single_node_start = self._find_position_single_node_start(l_SCC)
        object_cycles_finder = Find_cycles_in_SCC_for_stable_motifs(matrix_unsigned_of_SCC, 
                                                                    dict_i_node_array_contradicts_SCC, 
                                                                    i_position_of_single_node_start)
        l_l_i_cycles_containing_composite = object_cycles_finder.find_cycles_containing_composite_nodes()
        l_l_i_cycles_only_single = object_cycles_finder.find_cycles_only_single_nodes()
        
        l_l_i_cycles_containing_composite_modified = self._modify_cycles(l_l_i_cycles_containing_composite, l_SCC)
        l_l_i_cycles_only_single_modified = self._modify_cycles(l_l_i_cycles_only_single, l_SCC)

        return l_l_i_cycles_containing_composite_modified, l_l_i_cycles_only_single_modified
    
    def find_cycles(self):
        for l_SCC in self.l_l_SCCs:
            l_l_i_cycles_containing_composite, l_l_i_cycles_only_single  = self._find_cycles_in_SCC(l_SCC)
            self.l_l_i_cycles_containing_composite.extend(l_l_i_cycles_containing_composite)
            self.l_l_i_cycles_only_single.extend(l_l_i_cycles_only_single)
        
    def show_cycles_containing_composite_node(self):
        return self.l_l_i_cycles_containing_composite
    
    def show_cycles_only_single_nodes(self):
        return self.l_l_i_cycles_only_single
    
    
class Find_cycles_in_SCC_for_stable_motifs(Cycles_module.Find_cycles_in_SCC):
    def __init__(self, matrix_unsigned, dict_i_node_array_contradicts, i_position_of_single_node_start):
        Cycles_module.Find_cycles_in_SCC.__init__(self, matrix_unsigned)
        self.dict_i_node_array_contradicts = dict_i_node_array_contradicts
        self.i_position_of_single_node_start = i_position_of_single_node_start
        self.l_l_i_cycles_containing_composite = []
        self.l_l_i_cycles_only_single = []
        
    def _make_dict_of_opposing_state_containing_nodes(self, i_0_of_new_matrix):
        dict_i_node_set_contradicts_modified = {}
        for i_new, i_index in enumerate(range(i_0_of_new_matrix, len(self.matrix_unsigned))):
            array_indexes = self.dict_i_node_array_contradicts[i_index] - i_0_of_new_matrix
            dict_i_node_set_contradicts_modified[i_new] = set(array_indexes[array_indexes>=0])
        return dict_i_node_set_contradicts_modified
    
    def _find_cycles_on_node_over_i(self, i_0_of_new_matrix):
        matrix_over_node_i = np.matrix(self.matrix_unsigned[i_0_of_new_matrix:,i_0_of_new_matrix:])
        dict_i_node_set_contradicts_modified = self._make_dict_of_opposing_state_containing_nodes(i_0_of_new_matrix)
        object_cycle_finder = Find_cycles_containing_0_for_stable_motifs(matrix_over_node_i, dict_i_node_set_contradicts_modified)
        l_l_i_cycles = object_cycle_finder.find_cycles()

        return self._modify_cycles(l_l_i_cycles, i_0_of_new_matrix)
    
    def find_cycles_containing_composite_nodes(self):
        for i in range(self.i_position_of_single_node_start):
            self.l_l_i_cycles_containing_composite.extend(self._find_cycles_on_node_over_i(i))
        
        return self.l_l_i_cycles_containing_composite
    
    def find_cycles_only_single_nodes(self):
        for i in range(self.i_position_of_single_node_start, self.i_num_of_nodes):
            self.l_l_i_cycles_only_single.extend(self._find_cycles_on_node_over_i(i))
        
        return self.l_l_i_cycles_only_single

class Find_cycles_containing_0_for_stable_motifs(Cycles_module.Find_cycles_containing_0):
    def __init__(self, matrix_unsigned, dict_i_node_set_contradicts):
        Cycles_module.Find_cycles_containing_0.__init__(self, matrix_unsigned)
        self.dict_i_node_set_contradicts = dict_i_node_set_contradicts
        self.set_flow = set([])
    
    def _extend_flow(self, i_node):
        Cycles_module.Find_cycles_containing_0._extend_flow(self, i_node)
        self.set_flow.add(i_node)
        
    def _passable_case(self, i_next_edge):
        i_node_next = self.dic_i_start_array_ends[self.l_flow[-1]][i_next_edge]
        self.dic_i_start_i_count[self.l_flow[-1]] -= 1
        if i_node_next == 0:#it is a cycle containing 0
            self.l_connectable_to_0[-1] = True#l_flow[-1] node is connected to 0 node
            self.l_l_i_cycles.append(self.l_flow.copy())
        elif self.set_flow.intersection(self.dict_i_node_set_contradicts[i_node_next]):
            pass
        elif not self.array_blocked[i_node_next]:# not passed this node yet
            self._extend_flow(i_node_next)
            
    def _impassble_case(self):
        self.set_flow.discard(self.l_flow[-1])
        Cycles_module.Find_cycles_containing_0._impassble_case(self)
        