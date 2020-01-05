import numpy as np

class Topology:
    def __init__(self, s_name):
        self.s_name = s_name
        self.l_s_nodenames = []

    def show_nodenames(self):
        return self.l_s_nodenames

    def show_number_of_nodes(self):
        return len(self.l_s_nodenames)

    def set_nodenames(self, l_s_nodenames):
        self.l_s_nodenames.extend(l_s_nodenames)

    def add_nodename(self, s_nodename):
        self.l_s_nodenames.append(s_nodename)


class Unsigned_graph(Topology):
    #undirected edges informations are contained
    #edges having same start,end pair can exist
    def __init__(self, s_name):
        Topology.__init__(s_name)
        self.matrix_unsigned_graph = np.zeros((self.show_number_of_nodes(),self.show_number_of_nodes()))
        #(i,j) value means the number of edges j node -> i node

    def show_unsigned_graph_matrix_form(self):
        return self.matrix_unsigned_graph

    def set_unsigned_graph_matrix(self, matrix):
        self.matrix_unsigned_graph = np.array(matrix)


class Expanded_network(Unsigned_graph):
    def __init__(self,s_name):
        Undirected_grpah.__init__(s_name)
        self.s_suffix_of_on_node = "_1"
        self.s_suffix_of_on_node = "_0"
        self.s_andnode_connector = "__AND__"

        self.l_s_nodenames_single = []
        self.l_s_nodenames_composite = []
