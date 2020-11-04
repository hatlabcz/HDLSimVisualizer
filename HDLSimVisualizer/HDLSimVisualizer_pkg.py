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
from typing import Dict, Callable
import matplotlib.pyplot as plt


def int_to_slv(val: int, width: int) -> str:
    """
        int to std_logic_vector
    """
    return np.binary_repr(val, width)


def slv_to_int(s: str) -> int:
    """
        std_logic_vector to int
    """
    if s[0] == '0':  # positive
        return int(s, 2)
    else:  # negative
        width = len(s)
        return int(s, 2) - (1 << width)


def export_binary(file_name: str, data: np.array(int), data_width: int,
                  supersample: int):
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
    supersample : int
        data supersample.

    Returns
    -------
    None.

    """
    # fill in zeros if number of data points is not multiples of data_ss
    data = np.concatenate((data, np.zeros(len(data) % supersample, dtype=int)))
    with open(file_name, "w") as text_file:
        n_lines = len(data) // supersample
        for i in range(n_lines):
            w_line = ''
            for j in range(supersample):
                w_line = int_to_slv(data[i * supersample + j], data_width) \
                         + w_line
            text_file.write(w_line)
            if i != n_lines - 1:
                text_file.write('\n')


def import_binary(file_name: str, data_width: int,
                  supersample: int) -> np.array(int):
    """
    import data from the output of hdl simulation, change it to np.array

    Parameters
    ----------
    file_name : str
        name of target file.
    data_width : int
        width of the each std_logic_vector in the output file
    supersample : int
        data supersample.

    Returns
    -------
    data : np.array(int).

    """
    with open(file_name, "r") as text_file:
        data = []
        lines = text_file.readlines()
        for line in lines:
            r_line = line.strip()
            for i in range(supersample):
                r_data = r_line[-data_width:]
                r_line = r_line[:-data_width]
                data.append(slv_to_int(r_data))
    return np.array(data)


class HDLSim:
    def __init__(self, generics: Dict, data_in: np.array(int), sim_dir: str,
                 design_func: Callable, latency: int):
        """

        Parameters
        ----------
        generics : Dict
            dictionary that contains the generics of the HDL block
        data_in : np.array(int)
            input test data
        sim_dir : str
            HDL simulation directory that where the input and output data
            files are located
        design_func : Callable
            the function that does the job that the hdl code is expected to
            do, for compare and verify the HDL simulation result.
        latency : int
            latency of the HDL IP block in cycles
        """
        self.generics = generics
        self.input_width = generics["input_width"]
        self.input_ss = generics.get("input_ss", 1)
        self.output_width = generics["output_width"]
        self.output_ss = generics.get("output_ss", 1)
        self.sim_dir = sim_dir
        self.design_func = design_func
        # fill in zeros if number of data points is not multiples of supersample
        self.data_in = np.concatenate(
            (data_in, np.zeros(len(data_in) % self.input_ss, dtype=int)))
        self.cycles = len(data_in) // self.input_ss
        self.cyc_list = range(self.cycles)

        # expected output data
        data_out_exp = design_func(self.data_in)
        self.data_out_exp = np.roll(data_out_exp, latency * self.output_ss)

    def compareSimWithDesign(self,
                             sim_output_file: str = "output_results.txt",
                             plot: bool = True) -> bool:
        """
        compare HDL simulation data with the expected design output data.
        Parameters
        ----------
        sim_output_file : str
            file name of the output data from HDL simulation

        plot : bool
            when True, plot the comparision between simulation and design
        Returns
        -------
        pass_exam : bool
        """
        self.data_out = import_binary(self.sim_dir + sim_output_file,
                                      self.output_width,
                                      self.output_ss)
        print(self.data_out)
        if (self.data_out == self.data_out_exp).all:
            pass_exam = True
        else:
            pass_exam = False
        if plot:
            for i in range(self.output_ss):
                plt.figure(i)
                plt.plot(self.cyc_list, self.data_out_exp[i::self.output_ss],
                         '-', label='expected output')
                plt.plot(self.cyc_list, self.data_out[i::self.output_ss],
                         "*", label='simulation output')
                plt.legend()
        return pass_exam



def compareSimWithDesign(generics: Dict, latency: int,
                         expected_output: np.array(int), sim_output_file: str,
                         plot: bool = True):
    """
    compare HDL simulation data with the expected design output data.
    Parameters
    ----------
    generics : Dict
        dictionary that contains the generics of the HDL block
    expected_output : np.array(int)
        expected output result of the design function
    sim_output_file : str
        file name of the output data from HDL simulation
    plot : bool
        when True, plot the comparision between simulation and design
    Returns
    -------
    pass_exam : bool
    """
    output_width = generics["output_width"]
    output_ss = generics.get("output_ss", 1)
    data_out = import_binary(sim_output_file, output_width, output_ss)
    print(data_out)

    data_out_exp = np.roll(expected_output, latency * output_ss)
    print(data_out_exp)

    if (data_out == data_out_exp).all:
        pass_exam = True
    else:
        pass_exam = False

    cyc_list = range(len(data_out) // output_ss)
    if plot:
        for i in range(output_ss):
            plt.figure(i)
            plt.plot(cyc_list, data_out_exp[i::output_ss],
                     '-', label='expected output')
            plt.plot(cyc_list, data_out[i::output_ss],
                     "*", label='simulation output')
            plt.legend()
    return pass_exam