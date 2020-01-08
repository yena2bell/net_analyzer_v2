import numpy as np

def arraystate_to_int(array_state):
    array_binary_digit = np.array([pow(2,i) for i in range(len(array_state)-1,-1,-1)])
    return sum(array_state*array_binary_digit)

def int_to_arraystate(i_state, i_num_of_nodes):
    s_state = ("{:>0%d}" %i_num_of_nodes).format(bin(i_state)[2:])
    return np.array(list(s_state), dtype=int)

def int_to_arraystate_bool(i_state, i_num_of_nodes):
    s_state = ("{:>0%d}" %i_num_of_nodes).format(bin(i_state)[2:])
    return np.array([int(s) for s in s_state], dtype=bool)

def parse_string_to_list(s_string, l_s_components, b_permit_excepts=True):
    """parse the s_string to list.
    components of list are components of 'l_s_components'.
    if b_permit_excepts == False, the string should be composed of components of 'l_s_components' and spaces.
    if b_permit_excepts == True, component not included in l_s_components are found and parsed.
    component in 'l_s_components' are firstly parsed"""
    l_s_components_len_descending_order = l_s_components.copy()
    l_s_components_len_descending_order.sort(key=len, reverse=True)
    l_parsed_components = []
    
    i=0
    i_word_start = 0
    while i<len(s_string):
        for s_component in l_s_components_len_descending_order:
            if s_string[i:i+len(s_component)] == s_component:
                if i_word_start < i:
                    l_parsed_components.append(s_string[i_word_start:i])
                    i_word_start = i
                l_parsed_components.append(s_component)
                i += len(s_component)
                i_word_start += len(s_component)
                break
        else:
            if s_string[i].isspace():
                if i_word_start < i:
                    l_parsed_components.append(s_string[i_word_start:i])
                    i_word_start = i
                i += 1
                i_word_start += 1
            else:#s_string[i:i+alpha] is not space, and defined component
                if not b_permit_excepts:
                    raise ValueError("b_permit_except is setted False and not permitted component is in argument string")
                else:
                    i += 1
    if i_word_start < i:
        l_parsed_components.append(s_string[i_word_start:i])
    
    return l_parsed_components
