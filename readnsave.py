# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 14:21:59 2020

@author: zhaoz
"""

import scipy.io as sio
import pickle
import os.path
import inspect
# data_fold = 'dataset'
data_fold = 'data_combinesyn_oldstim'
TMSpop = 'TMSall'
plotpop = 'L23'
stimint = 'stim10'
# filename = "raster_spon_inon_{}.pkl".format(plotpop) 
filename = "raster_{}_{}_single_{}.pkl".format(TMSpop,stimint,plotpop)

#filename = "gsyn4.pkl"
#filename = "gsyn_TMS.pkl"

fn = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(fn))
df = os.path.join(path,data_fold,filename)
data = open(df,'rb')
data1 = pickle.load(data)


matname = 'raster_{}_{}_single_{}.mat'.format(TMSpop,stimint,plotpop)
# matname = "raster_spon_inon_{}.mat".format(plotpop) 
#matname = 'gsyn4.mat'
sio.savemat (os.path.join(path,data_fold,matname),{'data':data1})

