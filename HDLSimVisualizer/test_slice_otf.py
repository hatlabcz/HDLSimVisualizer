# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 20:46:24 2020

@author: Chao
"""

import numpy as np
import matplotlib.pyplot as plt
import HDLSimVisualizer_pkg as hsv
from HDLSimVisualizer_pkg import HDLSim

# ----------- generics ---------------------
generics = {"input_width": 16,
            "input_ss": 5,  # supersample
            "output_width": 15
            }
generics["output_ss"] = generics["input_ss"]
# --------- data----------------------------
input_data = np.arange(0, 100, 1)
offset_lower_bit = np.arange(0, 2, 1).repeat(50)

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


# ------------main---------------------
sim_in_dir = r"C:\Users\zctid.LAPTOP-150KME16\OneDrive\Lab\FPGA\VivadoPorjects\Demodulator\Demodulator\Demodulator.srcs\sim_1\imports\sim\\"
sim_out_dir = r"C:\Users\zctid.LAPTOP-150KME16\OneDrive\Lab\FPGA\VivadoPorjects\Demodulator\Demodulator\Demodulator.sim\sim_1\behav\xsim\\"
latency = 1

hsv.export_binary(sim_in_dir + "input_vectors.txt",
                  input_data, generics["input_width"], generics["input_ss"])

sim = HDLSim(generics, input_data, sim_out_dir, slice_otf, latency)
#
sim.compareSimWithDesign()

