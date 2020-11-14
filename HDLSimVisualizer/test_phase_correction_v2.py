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
PI = np.pi
# ----------- generics ---------------------
generics = {"input_width": 16,
            "input_ss": 1,  # supersample
            "output_width": 32
            }
generics["output_ss"] = generics["input_ss"]
# --------- data----------------------------
rand_seed = 10
np.random.seed(rand_seed)
n_data = 50


Ref_amp = 25000 + (np.random.rand(n_data) - 0.5) * 10000
Ref_phase = np.random.rand(n_data) * 2 * PI
RI = (Ref_amp * np.cos(Ref_phase)).astype(np.int)
RQ = (Ref_amp * np.sin(Ref_phase)).astype(np.int)

Sig_amp = 20000
Sig_phase = np.linspace(0, 2 * PI, n_data+1)[: n_data]
# Add or subtract Ref phase here
SI = (Sig_amp * np.cos(Sig_phase - Ref_phase)).astype(np.int)
SQ = (Sig_amp * np.sin(Sig_phase - Ref_phase)).astype(np.int)
data_phase = np.angle(SI + 1j*SQ)

expected_out_I = (Sig_amp * np.cos(Sig_phase)).astype(np.int)
expected_out_Q = (Sig_amp * np.sin(Sig_phase)).astype(np.int)


# ------------main---------------------
sim_in_dir = HOME + r"\OneDrive\Lab\FPGA\VivadoPorjects\Phase_Correction_v2\Phase_Correction.srcs\sim_1\imports\InputVectors\\"
# sim_out_dir = HOME + r"\OneDrive\Lab\FPGA\VivadoPorjects\Phase_Correction_v2\Phase_Correction.sim\sim_1\behav\xsim\\"
sim_out_dir = HOME + r"\OneDrive\Lab\FPGA\VivadoPorjects\Phase_Correction_v2\Phase_Correction.sim\sim_1\impl\func\xsim\\"
latency = 8

hsv.export_binary(sim_in_dir + "SI_vectors.txt",
                  SI, generics["input_width"], generics["input_ss"])
hsv.export_binary(sim_in_dir + "SQ_vectors.txt",
                  SQ, generics["input_width"], generics["input_ss"])
hsv.export_binary(sim_in_dir + "RI_vectors.txt",
                  RI, generics["input_width"], generics["input_ss"])
hsv.export_binary(sim_in_dir + "RQ_vectors.txt",
                  RQ, generics["input_width"], generics["input_ss"])


pass_check = hsv.compareSimWithDesign(generics, latency, expected_out_I*2**8,
                                    sim_out_dir+"output_results_1.txt")

pass_check = hsv.compareSimWithDesign(generics, latency, expected_out_Q*2**8,
                                    sim_out_dir+"output_results_2.txt")



pass_check = hsv.compareSimWithDesign(generics, latency, expected_out_I*2**8,
                                    sim_out_dir+"output_results_3.txt")
pass_check = hsv.compareSimWithDesign(generics, latency, expected_out_Q*2**8,
                                    sim_out_dir+"output_results_4.txt")

# plt.figure()
# plt.plot(SI, SQ)
# plt.plot(RI, RQ)
# plt.plot(*phase_correction(SI, SQ, RI, RQ))
# SIM_I = hsv.import_binary(sim_out_dir+"output_results_1.txt", 32, 1)
# SIM_Q = hsv.import_binary(sim_out_dir+"output_results_2.txt", 32, 1)
# sim_phase = np.unwrap(np.angle(SIM_I + 1j*SIM_Q))
#
# plt.figure()
# plt.plot(Sig_phase)
# plt.plot(sim_phase)