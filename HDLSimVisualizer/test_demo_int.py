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
generics = {"input_width": 31,
            "input_ss": 5,  # supersample
            "output_width": 35,
            "output_ss": 1
            }
# --------- data----------------------------
input_data = np.arange(0, 100, 1)


# --------- Design function -----------------
def demo_int(input_data):
    dout = [np.sum(input_data[i*5: i*5+10]) for i in range(len(input_data)//5)]
    return np.array(dout)


# ------------main---------------------
sim_dir = r"C:\Users\zctid.LAPTOP-150KME16\OneDrive\Lab\FPGA\VivadoPorjects" \
          r"\\Demodulator\Demodulator\Demodulator.sim\sim_1\behav\xsim\\"

hsv.export_binary("input_vectors.txt",
                  input_data, generics["input_width"], generics["input_ss"])

latency = 2
sim = HDLSim(generics, input_data, sim_dir, demo_int, latency)

sim.compareSimWithDesign()

