import numpy as np

def arraystate_to_int(array_state):
    array_binary_digit = np.array([pow(2,i) for i in range(len(array_state)-1,-1,-1)])
    return sum(array_state*array_binary_digit)

def int_to_arraystate(i_state, i_num_of_nodes):
    s_state = ("{:>0%d}" %i_num_of_nodes).format(bin(i_state)[2:])
    return np.array(list(s_state), dtype=int)
