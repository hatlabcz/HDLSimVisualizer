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
            "output_width": 16
            }
generics["output_ss"] = generics["input_ss"]
# --------- data----------------------------

n_data = 50
Ref_amp = 25000 + (np.random.rand(n_data) - 0.5) * 5000
Ref_phase = np.random.rand(n_data) * 2 * PI
RI = (Ref_amp * np.sin(Ref_phase)).astype(np.int)
RQ = (Ref_amp * np.cos(Ref_phase)).astype(np.int)

Sig_amp = 30000
Sig_phase = np.linspace(0, 2 * PI, n_data+1)[: n_data]
SI = (Sig_amp * np.sin(Ref_phase + Sig_phase)).astype(np.int)
SQ = (Sig_amp * np.cos(Ref_phase + Sig_phase)).astype(np.int)

# --------- Design function -----------------
def phase_correction(si, sq, ri, rq):
    R_norm = (ri + 1j * rq)/np.abs(ri + 1j * rq)
    S_complex = si + 1j * sq
    i = np.real(S_complex * R_norm.conj())
    q = np.imag(S_complex * R_norm.conj())
    return i, q

expected_out_I, expected_out_Q = phase_correction(SI, SQ, RI, RQ)

# ------------main---------------------
sim_in_dir = HOME + r"\OneDrive\Lab\FPGA\VivadoPorjects\Phase_Correction\Phase_Correction\Phase_Correction.srcs\sim_1\imports\sim\\"
sim_out_dir = HOME + r"\OneDrive\Lab\FPGA\VivadoPorjects\Phase_Correction\Phase_Correction\Phase_Correction.sim\sim_1\behav\xsim\\"
latency = 1

hsv.export_binary(sim_in_dir + "SI_vectors.txt",
                  SI, generics["input_width"], generics["input_ss"])
hsv.export_binary(sim_in_dir + "SQ_vectors.txt",
                  SQ, 32, generics["input_ss"])

plt.figure()
# plt.plot(SI, SQ)
plt.plot(*phase_correction(SI, SQ, RI, RQ))

# sim_pass = hsv.compareSimWithDesign(generics, latency, expected_out,
#                                     sim_out_dir+"output_results.txt")
#

