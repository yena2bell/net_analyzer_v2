# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 21:25:44 2020

@author: jwKim
"""

import os, sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
import net_analyzer_v2 as na2

l_nodes = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14']

lt_links=[('0', '11'),
 ('1', '13'),
 ('1', '7'),
 ('2', '11'),
 ('3', '0'),
 ('3', '2'),
 ('3', '5'),
 ('3', '6'),
 ('3', '7'),
 ('3', '8'),
 ('3', '9'),
 ('3', '10'),
 ('3', '11'),
 ('3', '12'),
 ('3', '13'),
 ('4', '9'),
 ('5', '9'),
 ('5', '13'),
 ('6', '13'),
 ('7', '2'),
 ('7', '3'),
 ('7', '4'),
 ('7', '12'),
 ('7', '14'),
 ('8', '14'),
 ('9', '0'),
 ('10', '3'),
 ('10', '4'),
 ('10', '14'),
 ('11', '0'),
 ('11', '12'),
 ('11', '5'),
 ('12', '9'),
 ('13', '9'),
 ('14', '7')]

l_t_links = [(l[0],None,l[-1]) for l in lt_links]

factory_test = na2.Factory("test")
factory_test.l_s_nodenames = l_nodes
factory_test.l_t_links = lt_links

graph_unsigned = factory_test.make_unsigned_graph()

l_l_s_cycles = na2.Cycles_module.find_cycles_unsigned_graph(graph_unsigned)