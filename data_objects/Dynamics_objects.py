from ..function_objects.Boolean_functions import Boolean_module

class Boolean_dynamics:
    def __init__(self, s_name):
        self.s_name = s_name
        self.l_s_nodenames = []
        self.l_s_inputnames = []
        self.dict_nodename_logictable = {}
        self.dict_nodename_orderdregulator = {}

    def set_nodenames(self, l_s_nodenames):
        self.l_s_nodenames.extend(l_s_nodenames)

    def set_Boolean_logic_table_to_node(self, s_target, t_ordered_regulator, i_Boolean_truth_table):
        self.dict_nodename_logictable[s_target] = i_Boolean_truth_table
        self.dict_nodename_orderdregulator[s_target] = t_ordered_regulator
        
    def show_nodenames(self):
        return self.l_s_nodenames
    
    def __repr__(self):
        return self.s_name

    def show_nodes_without_Boolean_logic(self):
        l_nodes_without_logic = []
        for s_nodename in self.l_s_nodenames:
            if s_nodename not in self.dict_nodename_logictable.keys():
                l_nodes_without_logic.append(s_nodename)

        return l_nodes_without_logic
    
    def show_Boolean_truth_table_of_node(self, s_nodename):
        i_truthtable = self.dict_nodename_logictable[s_nodename]
        t_regulators = self.dict_nodename_orderdregulator[s_nodename]
        return Boolean_module.show_Boolean_truthtable_form(i_truthtable, 
                                                           len(t_regulators), 
                                                           t_regulators, 
                                                           s_nodename)
    
    def show_Boolean_table_integer_of_node(self, s_nodename):
        return self.dict_nodename_logictable[s_nodename]
    
    def show_ordered_regulators_of_node(self, s_nodename):
        return self.dict_nodename_orderdregulator[s_nodename]

    
