# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:16:00 2020

@author: zhaoz
"""
import numpy as np
import pickle
numL5 = 100
numL23 = 100
numInh = 50
stim = '10'
stimint = 5
# np.random.seed(0)
L5_cellind = np.random.choice(numInh-1,stimint,replace=False) #20% L5 activated directly 
L5_cellind = L5_cellind.tolist()
# np.random.seed(1)
# L5_40 = np.random.choice(numL5-1,40,replace=False) #40% L5 activated directly 
# np.random.seed(2)
# L5_50 = np.random.choice(numL5-1,50,replace=False) #60% L5 activated directly

with open('Inh_cellind_stim_{}.data'.format(stim), 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(L5_cellind, filehandle)