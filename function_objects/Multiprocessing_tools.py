# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 15:58:45 2020

@author: jwKim
"""

import time

def decorator_semaphore_using_time(i_index, i_num_of_procs, i_interval, function_original):
    #0=< i_index < i_num_of_procs
    #i_interval is second
    def wrapper_function(*arg, **kwargs):
        while True:
            if int(time.time())%(i_num_of_procs*i_interval) == (i_index*i_interval):
                return function_original(*arg, **kwargs)
                break
    
    return wrapper_function
    