# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 22:32:27 2020

@author: zhaoz
"""
#load params from excel 
import pandas as pd
import os
import inspect
params_fold = 'params'
param_ver = 'nmdain_low4' # param edition
syn_ver = 'combinesyn'
connect_params_file = 'conn_traub_esser_{}_{}'.format(param_ver,syn_ver) #  'conn_traub_esser_nmdain_low_full2_inonly'/'conn_traub_esser'

fn = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(fn))
df = pd.read_csv(os.path.join(params_fold,connect_params_file + '.csv'))
