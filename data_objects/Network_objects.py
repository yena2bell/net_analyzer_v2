import pickle
import os
import numpy as np

class Topology:
    def __init__(self, s_name):
        self.s_name = s_name
        self.l_s_nodenames = []
        
    def __repr__(self):
        return self.s_name

    def show_nodenames(self):
        return self.l_s_nodenames

    def show_number_of_nodes(self):
        return len(self.l_s_nodenames)
    
    def __len__(self):
        return len(self.l_s_nodenames)

    def set_nodenames(self, l_s_nodenames):
        self.l_s_nodenames.extend(l_s_nodenames)

    def add_nodename(self, s_nodename):
        self.l_s_nodenames.append(s_nodename)
    
    def index_of_node(self, s_nodename):
        return self.l_s_nodenames.index(s_nodename)
    
    def save_using_pickle(self, s_address_of_folder_to_save):
        s_name_save = "pickle_save_"+str(self)+".bin"
        with open(os.path.join(s_address_of_folder_to_save,s_name_save), 'wb') as file_pickle:
            pickle.dump(self, file_pickle)


class Unsigned_graph(Topology):
    #undirected edges informations are contained
    #edges having same start,end pair can exist
    def __init__(self, s_name):
        Topology.__init__(self, s_name)
        self.matrix_unsigned_graph = np.zeros((len(self),len(self)))
        #(i,j) value means the number of edges j node -> i node

    def show_unsigned_graph_matrix_form(self):
        return self.matrix_unsigned_graph

    def set_unsigned_graph_matrix(self, matrix):
        self.matrix_unsigned_graph = np.matrix(matrix)
        
    def show_source_nodenames(self):
        l_index_sources = []
        for i in range(self.show_number_of_nodes()):
            if not self.show_unsigned_graph_matrix_form()[i,:].any():
                l_index_sources.append(i)
        return [self.show_nodenames()[j] for j in l_index_sources]
    
    def show_regulators_of_node(self, s_node):
        return [self.show_nodenames()[i] for i in self.show_indexes_of_regulators_of_node(self.index_of_node(s_node))]
    
    def show_indexes_of_regulators_of_node(self, i_node):
        matrix_row = self.show_unsigned_graph_matrix_form()[i_node,:]
        return np.nonzero(matrix_row)[1]


class Expanded_network(Unsigned_graph):
    def __init__(self,s_name):
        Unsigned_graph.__init__(self, s_name)
        self.s_suffix_of_on_node = "_1"
        self.s_suffix_of_off_node = "_0"
        self.s_andnode_connector = "__AND__"

        self.l_s_nodenames_single = []#'on' nodes are on odd indexes, "off" nodes are on even indexes
        self.l_s_nodenames_composite = []
        #self.l_s_nodenames = self.l_s_nodenames_single + self.l_s_nodenames_composite
    
    def set_single_nodenames(self, l_single_nodes):
        self.l_s_nodenames_single = l_single_nodes
    
    def set_composite_nodenames(self, l_composite_nodes):
        self.l_s_nodenames_composite = l_composite_nodes
    
    def show_single_nodenames(self):
        return self.l_s_nodenames_single
    
    def show_composite_nodenames(self):
        return self.l_s_nodenames_composite
    
    def show_suffix_of_on(self):
        return self.s_suffix_of_on_node
    
    def show_suffix_of_off(self):
        return self.s_suffix_of_off_node
    
    def show_connector(self):
        return self.s_andnode_connector
    
    def check_index_of_single_node(self, i_index):
        if (0 <= i_index) and (i_index < len(self.l_s_nodenames_single)):
            return True
        else:
            return False
    
    def check_single_node_index_is_on_state(self, i_index):
        if self.check_index_of_single_node(i_index):
            if i_index%2:# i_index is odd
                return True
            else:
                return False
        else:
            raise ValueError(str(i_index)+"("+self.show_single_nodenames()[i_index]+") is not single node")
        
    def show_original_nodename_from_index(self, i_index):
        if self.check_index_of_single_node(i_index):
            if self.check_single_node_index_is_on_state(i_index):
                return self.show_nodenames()[i_index][:-len(self.s_suffix_of_on_node)]
            else:
                return self.show_nodenames()[i_index][:-len(self.s_suffix_of_off_node)]
        else:
            raise ValueError(str(i_index)+"("+self.show_single_nodenames()[i_index]+") is not single node")
    
    def show_index_of_inverse_state_of_node(self, i_index):
        if self.check_index_of_single_node(i_index):
            #i_index%2 == 0 means i_index is even index so "off". to get index of "on" state node, add 1.
            #1 means "on". to get index of "off" state, add -1
            if self.check_single_node_index_is_on_state(i_index):
                return i_index - 1
            else:
                return i_index + 1
            #return i_index - 2*(i_index%2) + 1
        elif (i_index < len(self.l_s_nodenames)) and (len(self.l_s_nodenames_single) <= i_index):
            print(i_index," is composite node")
        else:
            raise ValueError(str(i_index)+" is out of range")
            
    def show_indexes_of_composite_node_containing_single_node(self, i_index):
        if self.check_index_of_single_node(i_index):
            array_index_composites = np.nonzero(self.show_unsigned_graph_matrix_form()[len(self.l_s_nodenames_single):,i_index])[0]
            return array_index_composites + len(self.l_s_nodenames_single)
        elif (i_index < len(self.l_s_nodenames)) and (len(self.l_s_nodenames_single) <= i_index):
            print(i_index," is composite node")
        else:
            raise ValueError(str(i_index)+" is out of range")
