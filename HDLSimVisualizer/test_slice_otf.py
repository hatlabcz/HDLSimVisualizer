# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 20:46:24 2020

@author: Chao
"""

import numpy as np
import matplotlib.pyplot as plt
import HDLSimVisualizer_pkg as hsv
from HDLSimVisualizer_pkg import HDLSim
from os.path import expanduser
HOME = expanduser("~")
# ----------- generics ---------------------
generics = {"input_width": 31,
            "input_ss": 5,  # supersample
            "output_width": 16
            }
generics["output_ss"] = generics["input_ss"]
# --------- data----------------------------
input_data = np.arange(0, 100, 1)
offset_lower_bit = np.arange(1, 3, 1).repeat(50)

# --------- Design function -----------------
def slice_otf(input_data):
    w_in = generics["input_width"]
    w_out = generics["output_width"]
    dout = []
    for i in range(len(input_data)):
        offset = offset_lower_bit[i]
        if w_out+offset>w_in:
            raise  ValueError

        din_bin  = hsv.int_to_slv(input_data[i], w_in)
        dout_bin = din_bin[-w_out-offset: -offset if offset!=0 else None]
        dout.append(hsv.slv_to_int(dout_bin))
    return np.array(dout)

expected_out = slice_otf(input_data)

# ------------main---------------------
sim_in_dir = HOME + r"\OneDrive\Lab\FPGA\VivadoPorjects\Demodulator\Demodulator\Demodulator.srcs\sim_1\imports\sim\\"
sim_out_dir = HOME + r"\OneDrive\Lab\FPGA\VivadoPorjects\Demodulator\Demodulator\Demodulator.sim\sim_1\behav\xsim\\"
latency = 1

hsv.export_binary(sim_in_dir + "input_vectors_1.txt",
                  input_data, generics["input_width"], generics["input_ss"])
hsv.export_binary(sim_in_dir + "input_vectors_2.txt",
                  offset_lower_bit, 32, generics["input_ss"])


sim_pass = hsv.compareSimWithDesign(generics, latency, expected_out,
                                    sim_out_dir+"output_results.txt")
#

