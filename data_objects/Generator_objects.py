import Dynamics_objects
import Network_objects

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
        Factory.__init__(s_name)
        self.s_address_data = None
        self.function_data_reading_adaptor = None
        self.function_converter_logics_to_Boolean = None
        self.dict_target_logic = {}

    def set_data_reading_adaptor(function_data_reading_adaptor):
        self.function_data_reading_adaptor = function_data_reading_adaptor

    def read_composite_logics_data(self, s_address):
        self.s_address_data = s_address
        with open(self.s_address_data, 'r') as file_data:
            self.dict_target_logic = self.function_data_reading_adaptor(file_data)

    def extract_data_from_logics(self):
        set_nodenames = set([])
        set_nodenames.update(self.dict_target_logic.keys())

        for s_target, s_logic in self.dict_target_logic.items():
            t_ordered_regulators, i_Boolean_table = self.convert_composite_logic_to_Boolean_logic(s_logic)
            self.dict_target_ordered_regulators[s_target] = t_ordered_regulators
            self.dict_target_Boolean_logic_table[s_target] = i_Boolean_table

            for s_regulator in t_ordered_regulators:
                if s_regulator not in set_nodenames:
                    #use log and caution
                    print("caution! ",s_regulator," the regulator of ",s_target," is not in keys of dict_target_logic")
                    set_nodenames.add(s_regulator)
                self.l_t_links.append((s_regulator, None, s_target))
        self.l_s_nodenames.extend(set_nodenames)

    def convert_composite_logic_to_Boolean_logic(self, s_logic):
        t_ordered_regulators, i_Boolean_logic_table = self.function_converter_logics_to_Boolean(s_logic)
        return t_ordered_regulators, i_Boolean_logic_table

            
class Factory_using_random_logics(Factory):
    pass

class Expanded_network_factory:
    def __init__(self, Boolean_dynamics):
        self.Boolean_dynamics = Boolean_dynamics
        
