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
        array_row = self.show_unsigned_graph_matrix_form()[self.index_of_node(s_node),:]
        return [self.show_nodenames()[i] for i in np.nonzero(array_row)[0]]


class Expanded_network(Unsigned_graph):
    def __init__(self,s_name):
        Unsigned_graph.__init__(self, s_name)
        self.s_suffix_of_on_node = "_1"
        self.s_suffix_of_off_node = "_0"
        self.s_andnode_connector = "__AND__"

        self.l_s_nodenames_single = []#'on' nodes are on odd indexes, "off" nodes are on even indexes
        self.l_s_nodenames_composite = []
    
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
