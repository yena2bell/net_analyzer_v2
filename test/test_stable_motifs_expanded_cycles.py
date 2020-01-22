# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 18:00:17 2020

@author: jwKim
"""

import os, sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
import net_analyzer_v2 as na2

from net_analyzer_v2.test import data_reader_200105

s_address_example = r"D:\my python\my library\net_analyzer_v2\test\stable_motif_example_200117.txt"
#s_address_example = r"D:\후속전략\norminal network_200105\COAD_logic.txt"

factory = na2.Factory_from_composite_logics("test_stable_motif")
factory.set_data_reading_strategy(data_reader_200105.data_reader_200105)
factory.set_regulators_extractor_strategy(data_reader_200105.find_regulator_from_logic_200105)
factory.set_converter_strategy(data_reader_200105.convert_logic_to_Boolean_table_200105)

factory.read_composite_logics_data(s_address_example)
factory.extract_data_from_logics()

unsigned_graph = factory.make_unsigned_graph()
Boolean_dynamics = factory.make_Boolean_dynamics()
factory_expanded = na2.Expanded_network_factory(unsigned_graph, Boolean_dynamics)
factory_expanded.make_all_nodes()#bottleneck
expanded_net = factory_expanded.make_expanded_network()

print(expanded_net.l_s_nodenames)

s_address_results = r"D:\my python\my library\net_analyzer_v2\test\test_200118_2.txt"

#l1, l2 = na2.Stable_motif_module.find_stable_motifs_using_expanded_net_cycles(expanded_net)
na2.Stable_motif_module.test_stable_motif_functions(expanded_net, s_address_results)
na2.Stable_motif_module.test2_stable_motif_functions(expanded_net)