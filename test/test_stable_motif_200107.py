# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 10:17:16 2020

@author: jwKim
"""

import os, sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
import net_analyzer_v2 as na2

from net_analyzer_v2.test import data_reader_200105

s_address_example = r"D:\my python\my library\net_analyzer_v2\test\stable_motif_example_200107.txt"

factory = na2.Factory_from_composite_logics("test_stable_motif")
factory.set_data_reading_strategy(data_reader_200105.data_reader_200105)
factory.set_regulators_extractor_strategy(data_reader_200105.find_regulator_from_logic_200105)
factory.set_converter_strategy(data_reader_200105.convert_logic_to_Boolean_table_200105)

factory.read_composite_logics_data(s_address_example)
factory.extract_data_from_logics()

unsigned_graph = factory.make_unsigned_graph()
Boolean_dynamics = factory.make_Boolean_dynamics()

l_SCCs = na2.SCC_module.decompose_to_SCC_unsigned_graph(unsigned_graph)

factory_expanded = na2.Expanded_network_factory(unsigned_graph, Boolean_dynamics)
factory_expanded.make_all_nodes()#bottleneck
expanded_net = factory_expanded.make_expanded_network()

print(expanded_net.l_s_nodenames)
print(expanded_net.show_unsigned_graph_matrix_form())

s_address_results = r"D:\my python\my library\net_analyzer_v2\test\stable_motif_results_200107.txt"

#l_dict_stable_motifs = na2.Stable_motif_module.find_stable_motifs(unsigned_graph, expanded_net, 1, None, [], s_address_results)

if __name__ == "__main__":
    l_dict_stable_motifs = na2.Stable_motif_module.find_stable_motifs(unsigned_graph, expanded_net, 1, None, [], s_address_results, 3)