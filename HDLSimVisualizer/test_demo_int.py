# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 20:46:24 2020

@author: Chao
"""

import numpy as np
import matplotlib.pyplot as plt
import HDL_Sim_pkg as hs

# ----------- generics ---------------------
input_width = 31
input_ss = 5 #supersample
output_width = 35
output_ss = 1

#--------- data----------------------------
input_data = np.arange(0, 100, 1)


#------------main---------------------
hs.export_binary("input_vectors.txt", input_data, input_width, input_ss )
def block_function(input_data):
    
    return 
    
output_data_expected = block_function(input_data)

