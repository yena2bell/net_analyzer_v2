print(__name__)

from ..function_objects.Boolean_functions import Boolean_module
from ..function_objects import Iterator_module

def data_reader_200105(file_data, separator=','):
    """ignore #
    ignore line without string
    target and logic are separated by separator"""
    file_data.readline()#delete first line

    dict_target_logic = {}

    for s_line in file_data:
        if '#' in s_line:
            s_line = s_line[:s_line.find('#')]
            #ignore Remarks
        s_line = s_line.strip()
        if len(s_line) == 0:
            continue

        s_target, s_logic = s_line.split(separator)
        dict_target_logic[s_target] = s_logic

    return dict_target_logic

def find_regulator_from_logic_200105(s_logic):
    s_logic = s_logic.strip()
    s_logic = s_logic.replace("("," ( ")
    s_logic = s_logic.replace(")"," ) ")
    s_logic = s_logic.replace("|"," | ")
    s_logic = s_logic.replace("&"," & ")
    s_logic = s_logic.replace("!"," ! ")
    l_s_components = s_logic.split()
    l_s_not_nodes = ['(',')','|','&','!']
    for i in range(len(l_s_components)-1, -1, -1):
        if l_s_components[i] in l_s_not_nodes:
            l_s_components.pop(i)
    
    t_regulators = tuple(set(l_s_components))
    return t_regulators

def convert_logic_to_Boolean_table_200105(s_logic, t_regulators):
    s_logic = s_logic.replace('!', " not ")
    s_logic = s_logic.replace('&', " and ")
    s_logic = s_logic.replace('|', " or ")
    i = 0
    i_Boolean_table = 0
    for array_state in Iterator_module.iterator_all_state(len(t_regulators), {}):
        dict_node_state = dict(zip(t_regulators,array_state[::-1]))
        if eval(s_logic, dict_node_state):
            i_Boolean_table += pow(2, i)
        i += 1
    
    return i_Boolean_table 