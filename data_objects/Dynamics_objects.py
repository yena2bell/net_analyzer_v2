class Boolean_dynamics:
    def __init__(self, s_name):
        self.s_name = s_name
        self.l_s_nodenames = []
        self.l_s_inputnames = []
        self.dict_nodename_logictable = {}
        self.dict_nodename_orderdregulator = {}

    def set_nodenames(selt, l_s_nodenames):
        self.l_s_nodenames.extend(l_s_nodenames)

    def set_Boolean_logic_table_to_node(self, s_target, t_ordered_regulator, i_Boolean_truth_table):
        self.dict_nodename_logictable[s_target] = i_Boolean_truth_table
        self.dict_nodename_orderdregulator[s_target] = t_ordered_regulator

    def show_nodes_without_Boolean_logic(self):
        l_nodes_without_logic = []
        for s_nodename in l_s_nodenames:
            if s_nodename not in self.dict_nodename_logictable.keys():
                l_nodes_without_logic.append(s_nodename)

        return l_nodes_without_logic

    
