from . import Dynamics_objects
from . import Network_objects
from ..function_objects.Boolean_functions import Boolean_module

class Factory:
    def __init__(self, s_name):
        self.s_name = s_name
        self.l_s_nodenames = []
        self.l_t_links = [] #(start, modality, end)
        self.dict_target_ordered_regulators = {}
        self.dict_target_Boolean_logic_table = {}

    def make_Boolean_dynamics(self):
        Boolean_dynamics_new = Dynamics_objects.Boolean_dynamics(self.s_name)
        Boolean_dynamics_new.set_nodenames(self.l_s_nodenames)
        for s_node in self.dict_target_ordered_regulators.keys():
            Boolean_dynamics_new.set_Boolean_logic_table_to_node(s_node,
                                                                 self.dict_target_ordered_regulators[s_node],
                                                                 self.dict_target_Boolean_logic_table[s_node])
        return Boolean_dynamics_new

    def make_unsigned_graph(self):
        Unsigned_graph_new = Network_objects.Unsigned_graph(self.s_name)
        Unsigned_graph_new.set_nodenames(self.l_s_nodenames)

        l_zero_row = [0]*len(self.l_s_nodenames)
        matrix_unsigned_graph = [l_zero_row.copy() for _ in self.l_s_nodenames]
        for t_link in self.l_t_links:
            j = self.l_s_nodenames.index(t_link[0])#start
            i = self.l_s_nodenames.index(t_link[-1])#end
            matrix_unsigned_graph[i][j] += 1
        Unsigned_graph_new.set_unsigned_graph_matrix(matrix_unsigned_graph)

        return Unsigned_graph_new


class Factory_from_composite_logics(Factory):
    def __init__(self, s_name):
        Factory.__init__(self, s_name)
        self.s_address_data = None
        self.function_data_reading_adaptor = None
        self.function_regulator_extractor = None
        self.function_converter_logics_to_Boolean = None
        self.dict_target_logic = {}

    def set_data_reading_strategy(self, function_data_reading_adaptor):
        self.function_data_reading_adaptor = function_data_reading_adaptor
        
    def set_regulators_extractor_strategy(self, function_regulator_extractor):
        self.function_regulator_extractor = function_regulator_extractor
        
    def set_converter_strategy(self, function_converter_logic_to_Boolean):
        self.function_converter_logics_to_Boolean = function_converter_logic_to_Boolean

    def read_composite_logics_data(self, s_address):
        self.s_address_data = s_address
        with open(self.s_address_data, 'r') as file_data:
            self.dict_target_logic = self.function_data_reading_adaptor(file_data)

    def extract_data_from_logics(self):
        set_nodenames = set([])
        set_nodenames.update(self.dict_target_logic.keys())

        for s_target, s_logic in self.dict_target_logic.items():
            t_ordered_regulators = self.extract_regulators_from_logics(s_logic)
            i_Boolean_table = self.convert_composite_logic_to_Boolean_logic(s_logic,
                                                                            t_ordered_regulators)
            self.dict_target_ordered_regulators[s_target] = t_ordered_regulators
            self.dict_target_Boolean_logic_table[s_target] = i_Boolean_table

            for s_regulator in t_ordered_regulators:
                if s_regulator not in set_nodenames:
                    #use log and caution
                    print("caution! ",s_regulator," the regulator of ",s_target," is not in keys of dict_target_logic")
                    set_nodenames.add(s_regulator)
                self.l_t_links.append((s_regulator, None, s_target))
        self.l_s_nodenames.extend(set_nodenames)
        
    def extract_regulators_from_logics(self, s_logic):
        t_ordered_regulators = self.function_regulator_extractor(s_logic)
        return t_ordered_regulators

    def convert_composite_logic_to_Boolean_logic(self, s_logic, t_ordered_regulators):
        i_Boolean_logic_table = self.function_converter_logics_to_Boolean(s_logic,
                                                                          t_ordered_regulators)
        return i_Boolean_logic_table

            
class Factory_using_random_logics(Factory):
    pass

class Expanded_network_factory:
    #no logic node (maybe source node) has single node but no upper single node to that node.
    #if logic of the node is itself (i.e. gene1 = gene1) it makes self loop to single node of this node
    #if logic is always true or false, then the single node has no regulator(in case always false) or has all single node of regulators in unsigned graph
    #for example, gene1 has regulators gene2,gene3 in unsigned graph and its logic results in True,
    #(gene1,"on") has regulators (gene2,"on"),(gene2,"off"),(gene3,"on"), (gene3,"off") in expanded network.
    #(gene1,"off") has no regulators
    def __init__(self, Unsigned_graph, Boolean_dynamics):
        self.unsigned_graph = Unsigned_graph
        self.Boolean_dynamics = Boolean_dynamics
        self.l_t_single_nodes = []#example of single node ("gene","on") or ("gene","off")
        self.l_t_composite_nodes = []#example of composite node(("gene","on"),("gene2","off"),("gene3","on"))
        self.l_nodes = []# == self.l_t_single_nodes+self.l_t_composite_nodes
        self.l_t_links = []#t_link = (i, j) which means ith node -> jth node. i and j are the index of node in self.l_nodes
            
    def make_all_nodes(self):
        print("start making expanded nodes and connection")
        self._check_node_without_logic()
        self._make_single_nodes()
        self._make_composite_nodes_and_connect_nodes()
        print("expanded node and connections are all calculated")
        
    def make_expanded_network(self):
        #do make_all_nodes function before doing this function.
        expanded_network_new = Network_objects.Expanded_network(str(self.Boolean_dynamics))
        s_suffix_on = expanded_network_new.show_suffix_of_on()
        s_suffix_off = expanded_network_new.show_suffix_of_off()
        s_andnode_connector = expanded_network_new.show_connector()
        
        l_s_single_nodes = []
        for t_single_node in self.l_t_single_nodes:
            if t_single_node[1] == "on":
                l_s_single_nodes.append(t_single_node[0]+s_suffix_on)
            elif t_single_node[1] == "off":
                l_s_single_nodes.append(t_single_node[0]+s_suffix_off)
            else:
                raise ValueError("why?(1)")
        expanded_network_new.set_single_nodenames(l_s_single_nodes)
        
        l_s_composite_nodes = []
        for t_composite_node in self.l_t_composite_nodes:
            l_composite_node = []
            for t_single_node in t_composite_node:
                if t_single_node[1] == "on":
                    l_composite_node.append(t_single_node[0]+s_suffix_on)
                elif t_single_node[1] == "off":
                    l_composite_node.append(t_single_node[0]+s_suffix_off)
                else:
                    raise ValueError("why?(2)")
            l_s_composite_nodes.append(s_andnode_connector.join(l_composite_node))
        expanded_network_new.set_composite_nodenames(l_s_composite_nodes)
        
        expanded_network_new.set_nodenames(l_s_single_nodes+l_s_composite_nodes)
        
        l_zero_row = [0]*len(self.l_nodes)
        matrix_unsigned_graph = [l_zero_row.copy() for _ in self.l_nodes]
        for t_link in self.l_t_links:
            j = t_link[0]#start
            i = t_link[-1]#end
            matrix_unsigned_graph[i][j] += 1
        expanded_network_new.set_unsigned_graph_matrix(matrix_unsigned_graph)
        
        return expanded_network_new
        

    def _check_node_without_logic(self):
        l_s_node_without_logic = self.Boolean_dynamics.show_nodes_without_Boolean_logic()
        l_s_node_source = self.unsigned_graph.show_source_nodenames()
        set_no_logic_not_source = set(l_s_node_without_logic).difference(set(l_s_node_source))
        if set_no_logic_not_source:
            raise ValueError("nodes "+str(set_no_logic_not_source)+" have no logic data although they are not source node")

    def _make_single_nodes(self):
        for s_node in self.Boolean_dynamics.show_nodenames():#let odd indexes are 'on' node, and even indexes are 'off' node
            self.l_t_single_nodes.append((s_node,"off"))
            self.l_t_single_nodes.append((s_node,"on"))
            
    def _make_composite_nodes_and_connect_nodes(self):
        i_count=0
        for single_node in self.l_t_single_nodes:
            i_count += 1
            print(i_count,"/",len(self.l_t_single_nodes))
            self._make_upstream_nodes_of_single_node(single_node)
        
        self.l_nodes = self.l_t_single_nodes + self.l_t_composite_nodes
    
    def _make_upstream_nodes_of_single_node(self, single_node):
        print(single_node[0]+"'s "+single_node[1]+" state calculation starts")
        i_logic = self.Boolean_dynamics.show_Boolean_table_integer_of_node(single_node[0])
        t_regulators = self.Boolean_dynamics.show_ordered_regulators_of_node(single_node[0])
        if single_node[1] == "on":
            l_logic = Boolean_module.get_minimize_Boolean_logic_from_truthtable(i_logic, 
                                                                                t_regulators, 
                                                                                algorithm="Quine_McCluskey")
        elif single_node[1] == "off":
            l_logic = Boolean_module.get_minimize_Boolean_logic_from_inversed_truthtable(i_logic, 
                                                                                         t_regulators, 
                                                                                         algorithm="Quine_McCluskey")
        else:
            raise ValueError("single node has only 'on','off' in second component!")
        print(single_node[0]+"'s "+single_node[1]+" state has "+" ".join(l_logic))
        l_expanded_nodes_regulators = self._decompose_l_logic_to_expanded_nodes(l_logic)
        l_expanded_nodes_regulators = self._add_decomposed_nodes_to_list(l_expanded_nodes_regulators)
        self._connect_decomposed_nodes(l_expanded_nodes_regulators, single_node)
        
    
    def _decompose_l_logic_to_expanded_nodes(self, l_logic_argument, 
                                            dict_operators={"not":"NOT",
                                                            "and":"AND",
                                                            "or":"OR",
                                                            'left_blacket':'(',
                                                            'right_blacket':')'}):
        #l_logic has form of ((A and B and...) or (C and (not d)...)...) or (A and B) or (A or (not B))
        l_logic = l_logic_argument.copy()
        if l_logic == [0]:
            return []
        elif l_logic == [1]:
            return ["all"]
        else:
            for i in range(len(l_logic)-1,-1,-1):
                if l_logic[i] == dict_operators["not"]:
                    l_logic = l_logic[:i]+[(l_logic[i+1], "off")]+l_logic[i+2:]
            for i in range(len(l_logic)-1,-1,-1):
                if (l_logic[i] not in dict_operators.values()) and not self._is_simple_node(l_logic[i]):#find node component except already converted nodes
                    l_logic = l_logic[:i]+[(l_logic[i], "on")]+l_logic[i+1:]

            while (dict_operators["and"] in l_logic) or (dict_operators["right_blacket"] in l_logic):
                i_right_blacket = l_logic.index(dict_operators["right_blacket"])
                for i in range(i_right_blacket,-1,-1):
                    if l_logic[i] == dict_operators["left_blacket"]:
                        i_left_blacket = i
                        break
                l_logic_between_blacket = list(l_logic[i_left_blacket+1: i_right_blacket])
                if len(l_logic_between_blacket) == 1 and self._is_simple_node(l_logic_between_blacket[0]):
                    l_logic = l_logic[:i_left_blacket] +l_logic_between_blacket + l_logic[i_right_blacket+1:]
                elif (dict_operators["and"] in l_logic_between_blacket) and not (dict_operators["or"] in l_logic_between_blacket):
                    l_tmp = [logic_part for logic_part in l_logic_between_blacket if logic_part != dict_operators["and"]]
                    l_logic = l_logic[:i_left_blacket] +[tuple(l_tmp)] + l_logic[i_right_blacket+1:]
                elif (dict_operators["or"] in l_logic_between_blacket) and not (dict_operators["and"] in l_logic_between_blacket):
                    l_logic.pop(i_right_blacket)
                    l_logic.pop(i_left_blacket)
                else:
                    raise ValueError(str(l_logic_argument)+" can't be processed in this functions")
            
            l_expanded_nodes = [logic_part for logic_part in l_logic if logic_part != dict_operators["or"]]
            
            return l_expanded_nodes
                
    
    def _add_decomposed_nodes_to_list(self, l_expanded_nodes):
        for i in range(len(l_expanded_nodes)-1,-1,-1):
            expanded_node = l_expanded_nodes[i]
            if expanded_node == "all": #when l_logic == [1]
                pass
            elif self._is_simple_node(expanded_node):#single nodes
                pass
            else:#composite nodes
                for t_composite_node in self.l_t_composite_nodes:#avoid duplication of composite node
                    if set(t_composite_node) == set(expanded_node):
                        l_expanded_nodes[i] = t_composite_node
                        break
                else:
                    self.l_t_composite_nodes.append(expanded_node)
        
        return l_expanded_nodes
    
    def _connect_decomposed_nodes(self, l_expanded_nodes, expanded_node_end):
        i_index_end = self.l_t_single_nodes.index(expanded_node_end)
        for expanded_node in l_expanded_nodes:
            if expanded_node == "all":
                s_nodename = expanded_node_end[0]
                l_regulators = self.unsigned_graph.show_regulators_of_node(s_nodename)
                for s_regulator in l_regulators:
                    i_index_start = self.l_t_single_nodes.index((s_regulator,"on"))
                    self.l_t_links.append((i_index_start,i_index_end))
                    i_index_start = self.l_t_single_nodes.index((s_regulator,"off"))
                    self.l_t_links.append((i_index_start,i_index_end))
                    
            elif self._is_simple_node(expanded_node):
                i_index_start = self.l_t_single_nodes.index(expanded_node)
                self.l_t_links.append((i_index_start,i_index_end))
            else:
                i_index_composite = self.l_t_composite_nodes.index(expanded_node)
                i_index_composite += len(self.l_t_single_nodes)#by adding this, i_index_composite become index in l_nodes
                self.l_t_links.append((i_index_composite,i_index_end))
                for single_node in expanded_node:
                    i_index_start = self.l_t_single_nodes.index(single_node)
                    if (i_index_start,i_index_composite) not in self.l_t_links:
                        self.l_t_links.append((i_index_start,i_index_composite))
                
    
    def _is_simple_node(self, expanded_node):
        l_onoff = ["on","off"]
        if (len(expanded_node)==2) and (expanded_node[1] in l_onoff):
            return True
        else:
            return False
