# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 23:22:43 2020

@author: Chao

This package contains helper functions and classes that can be used to verify 
and visualize the simulation results from HDL simulators. The purpose is to 
make it easier to generate data file for simulation input, import simulation 
output and compare it with expected block outputs.
"""
import numpy as np
import matplotlib.pyplot as plt


def int_to_slv(val: int, width: int)->str:
    """
        int to std_logic_vector
    """
    return np.binary_repr(val, width)

def slv_to_int(s: str, width:int)->int:
    """
        std_logic_vector to int
    """
    if s[0] == '0': # positive
        return int(s,2)
    else: # negative
        return int(s,2)-(1<<width)

def export_binary(file_name: str, data: np.array(int), data_width: int , data_ss: int):
    """
    export data to a txt file. Each line in the txt file is a super sampled 
    std_logic_vector data.

    Parameters
    ----------
    file_name : str
        name of target file.
    data : np.array(int)
        data to be exported.
    data_width : int
        width of the std_logic_vector that the data is going to be writted as
    data_ss : int
        data supersample.

    Returns
    -------
    None.

    """
    # fill in zeros if number of data points is not multiples of data_ss
    data = np.concatenate((data, np.zeros(len(data) % data_ss, dtype=int))) 
    with open(file_name, "w") as text_file:
        n_lines = len(data) // data_ss
        for i in range(n_lines):
            w_line = ''
            for j in range(data_ss):
                w_line += int_to_slv(data[i * data_ss + j], data_width)
            text_file.write(w_line)
            if i != n_lines-1:
                text_file.write('\n')
                
def import_binary(file_name: str, data_width: int , data_ss: int) -> np.array(int):
    """
    import data from the output of hdl simulation, change it to np.array

    Parameters
    ----------
    file_name : str
        name of target file.

    data_width : int
        width of the each std_logic_vector in the output file
    data_ss : int
        data supersample.

    Returns
    -------
    data : np.array(int).

    """
    data = np.zeros(10)
    return data

# TODO: a class that is initialized with generaic dictionary, input data, 
#       simulation directory, and block function