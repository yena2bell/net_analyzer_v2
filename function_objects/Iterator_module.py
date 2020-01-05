import numpy as np

import Converter_module

def iterator_all_state(i_num_nodes, dict_perturbed_nodes,
                       i_num_processes=1, i_ith_process=0):
    """dict_perturbed_nodes = {index_of_perturbed_node: state_of_perturbed_node}
    return state as array form."""

    l_index_perturbed = list(dict_perturbed_nodes.keys())
    l_index_perturbed.sort()

    if len(set(l_index_perturbed)) < len(l_index_perturbed):
        raise ValueError("Error! some perturbation has duplication!")

    i_num_nodes_changable = i_num_nodes - len(l_index_perturbed)

    l_l_matrix = []
    i_position_of_1 = 0
    for i_row in range(i_num_nodes_changable):
        l_row = [0]*i_num_nodes
        while i_position_of_1 in l_index_perturbed:
            i_position_of_1 += 1
        l_row[i_position_of_1] = 1
        i_position_of_1 += 1
        l_l_matrix.append(l_row)
    matrix_n_nodes_to_m_nodes = np.array(l_l_matrix, dtype=int)

    array_state_with_perturbation = np.zeros((i_num_nodes,), dtype=int)
    for i_index in l_index_perturbed:
        array_state_with_perturbation[i_index] = dict_perturbed_nodes[i_index]

    #small speed up code
    if l_index_perturbed:
        if array_state_with_perturbation.any():#one of perturbed state is on
            perturbation_adder = _some_perturbed_to_1
        else:
            perturbation_adder = _all_perturbed_state_0
    else:#no perturbation
        perturbation_adder = _no_perturbation

    for i_state in range(i_ith_process, pow(2,i_num_nodes_changable), i_num_processes):
        array_state = Converter_module.int_to_arraystate(i_state, i_num_nodes_changable)
        yield perturbation_adder(array_state,
                                matrix_n_nodes_to_m_nodes,
                                array_state_with_perturbation)
    
def _no_perturbation(array_state, matrix, array_perturbed_state):
    return array_state

def _all_perturbed_state_0(array_state, matrix, array_perturbed_state):
    return np.matmul(array_state, matrix)

def _some_perturbed_to_1(array_state, matrix, array_perturbed_state):
    return np.matmul(array_state, matrix) + array_perturbed_state

    
def generator_combination_num_in_defined_1(i_all_candiates, i_num_of_selected,
                                           i_num_processes=1, i_ith_process=0):
    """ make generator giving integer which has 'i_num_of_selected' of 1 when converted to binaray form.
    and that integer's binary form has digits lesser than n"""
    if i_all_candiates < i_num_of_selected:
        raise ValueError("n should be larger or equal to i_num_of_1")
    if i_all_candiates<=0:
        raise ValueError("n shoule be larger than 0")
    
    i_position_of_smallest_1 = 0
    i_position_of_smallest_0_after_first_1 = int(i_num_of_selected)
    i_combination = pow(2,int(i_num_of_selected))-1
    i_end_combination = i_combination * pow(2,(int(i_all_candiates)-int(i_num_of_selected)))

    i_count = 0
    if i_count%i_num_processes == i_ith_process:
        yield i_combination
    
    while i_combination < i_end_combination:
        if i_position_of_smallest_0_after_first_1 == 1:
            i_combination += pow(2, i_position_of_smallest_1)
            i_position_of_smallest_1 += 1
        else:
            i_combination += pow(2, i_position_of_smallest_1 + i_position_of_smallest_0_after_first_1 - 1)
            i_sum = i_position_of_smallest_1 + i_position_of_smallest_0_after_first_1
            i_combination = (i_combination>>i_sum)*pow(2,i_sum) + pow(2, i_position_of_smallest_0_after_first_1 - 1) -1
            i_position_of_smallest_1 = 0
            
        i_position_of_smallest_0_after_first_1 = 1
        while (i_combination >> (i_position_of_smallest_1 + i_position_of_smallest_0_after_first_1))%2 == 1:
            i_position_of_smallest_0_after_first_1 += 1

        i_count += 1
        if i_count%i_num_processes == i_ith_process:
            yield i_combination    
    
