# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 09:14:16 2020

@author: zhaoz
"""
import pickle
from netpyne import specs, sim
from loadfile import df
from cell2ind import cell2ind
# import os
# import inspect
# get file direction 
# fn = inspect.getframeinfo(inspect.currentframe()).filename
# path = os.path.dirname(os.path.abspath(fn))
# data_fold = 'dataset'
# datadir = os.path.join(path,data_fold)
#Network parameters
netParams = specs.NetParams() # object of class NetParams to store the network parameters

#Create three neuron population :L23exc, L5exc and Inh
netParams.popParams['L23exc'] = {'cellType': 'L23exc', 'numCells': 100, 'cellModel': 'L23exc_esser'}
netParams.popParams['L5exc'] = {'cellType':'L5exc','numCells':100, 'cellModel': 'L5exc_esser'}
netParams.popParams['Inh'] = {'cellType': 'Inh', 'numCells': 50, 'cellModel': 'I_esser'}

#Create poisson input population: inL23exc, inL5exc and inInh
netParams.popParams['inL23exc'] = {'cellModel': 'NetStim', 'interval': 1000/8, 'noise': 1, 'numCells': 100,'start': 0}  # NetsStim
netParams.popParams['inL5exc'] = {'cellModel': 'NetStim', 'interval': 1000/10, 'noise': 1, 'numCells': 100,'start': 0}  # NetsStim
netParams.popParams['inInh'] = {'cellModel': 'NetStim', 'interval': 1000/16, 'noise': 1, 'numCells': 100,'start': 0}  # NetsStim

#Define cellRule 
cellRule = {'conds': {'cellType': 'L23exc', 'cellModel': 'L23exc_esser'},  'secs': {}} 						# cell rule dict
cellRule['secs']['soma'] = {'geom': {}, 'ions':{}, 'pointps': {}, 'vinit':{}}  												# soma params dict
cellRule['secs']['soma']['geom'] = {'diam':1500, 'L': 18.8, 'Ra':123.0,'cm':15}
cellRule['secs']['soma']['pointps']['esser'] = {'mod':'esser_mech', 
              'theta_eq' : -53,'tau_theta' : 2,'tau_spike' : 1.75/15,'tau_m' : 15/15,'gNa_leak' : 0.14,
              'gK_leak' : 1.0, 'tspike' : 2.0}  					
cellRule['secs']['soma']['ions'] = {'na':{'e':30.0},'k':{'e':-90}}
cellRule['secs']['soma']['vinit'] = -75.263
netParams.cellParams['L23exc_esser_rule'] = cellRule

cellRule = {'conds': {'cellType': 'L5exc', 'cellModel': 'L5exc_esser'},  'secs': {}} 						# cell rule dict
cellRule['secs']['soma'] = {'geom': {}, 'ions':{}, 'pointps': {}, 'vinit':{}}  												# soma params dict
cellRule['secs']['soma']['geom'] = {'diam':1500, 'L':18.8, 'Ra':123.0,'cm':13}
cellRule['secs']['soma']['pointps']['esser'] = {'mod':'esser_mech', 
              'theta_eq' : -53,'tau_theta' : 0.5,'tau_spike' : 0.6/13,'tau_m' : 13/13,'gNa_leak' : 0.14,
              'gK_leak' : 1.3, 'tspike' : 0.75}  					
cellRule['secs']['soma']['ions'] = {'na':{'e':30.0},'k':{'e':-90}}
cellRule['secs']['soma']['vinit'] = -78.33
netParams.cellParams['L5exc_esser_rule'] = cellRule 			# add dict to list of cell parameters

cellRule = {'conds': {'cellType': 'Inh', 'cellModel': 'I_esser'},  'secs': {}} 						# cell rule dict
cellRule['secs']['soma'] = {'geom': {}, 'ions':{}, 'pointps': {}, 'vinit':{}}  												# soma params dict
cellRule['secs']['soma']['geom'] = {'diam':1500, 'L': 18.8, 'Ra':123.0,'cm':7}
cellRule['secs']['soma']['pointps']['esser'] = {'mod':'esser_mech', 
              'theta_eq' : -54,'tau_theta' : 1,'tau_spike' : 0.48/7,'tau_m' : 7/7,'gNa_leak' : 0.2,
              'gK_leak' : 1.0, 'tspike' : 0.75}  					
cellRule['secs']['soma']['ions'] = {'na':{'e':30.0},'k':{'e':-90}}
cellRule['secs']['soma']['vinit'] = -75.263
netParams.cellParams['Inh_rule'] = cellRule

# Read params from excel and create synaptic connections in a loop 
pre_name = df["pre_name"]
post_name = df["post_name"]
syn_type = df["pre_type"]
delay_mean = df["delay_mean"]
delay_std = df["delay_std"]
strength = df["strength"]
p = df["p"]
wratio = df["wratio"]

# Synaptic mechanism parameters
netParams.synMechParams['AMPA'] = {'mod': 'Exp2Syn_esser','gpeak':0.1, 'tau_m': 1,'tau1': 0.5,'tau2': 2.4, 'e': 0} #excitatory synaptic mechanism
# netParams.synMechParams['NMDA'] = {'mod': 'NMDA_esser','gpeak':0.1, 'tau_m': 1,'tau1': 4,'tau2': 40, 'e': 0} #excitatory synaptic mechanism
# netParams.synMechParams['GABAA'] = {'mod': 'Exp2Syn_esser','gpeak':0.33, 'tau_m': 1,'tau1': 1,'tau2': 7, 'e': -70} #Inhibitory synaptic mechanism
# netParams.synMechParams['GABAB'] = {'mod': 'Exp2Syn_esser','gpeak':0.0132, 'tau_m': 1,'tau1': 60,'tau2': 200, 'e': -90} #inhibitory synaptic mechanism
netParams.synMechParams['E'] = {'mod': 'Exc_esser','gpeak_AMPA':0.1, 'tau_m': 1,'tau1_AMPA': 0.5,'tau2_AMPA': 2.4, 'e_AMPA': 0, 
                                  'gpeak_NMDA':0.1,'tau1_NMDA': 4,'tau2_NMDA': 40, 'e_NMDA': 0, 'wratio': wratio[1]} #excitatory synaptic mechanism
netParams.synMechParams['I'] = {'mod': 'Inh_esser','gpeak_GABAA':0.33, 'tau_m': 1,'tau1_GABAA': 1,'tau2_GABAA': 7, 'e_GABAA': -70,
                                  'gpeak_GABAB':0.0132, 'tau1_GABAB': 60,'tau2_GABAB': 200, 'e_GABAB': -90 , 'wratio':wratio[8]} #Inhibitory synaptic mechanism

# netParams.synMechParams['inL5E'] = netParams.synMechParams['E']
# netParams.synMechParams['inL5E']['wratio'] = wratio[9]

netParams.synMechParams['inL5E'] = {'mod': 'Exc_esser','gpeak_AMPA':0.1, 'tau_m': 1,'tau1_AMPA': 0.5,'tau2_AMPA': 2.4, 'e_AMPA': 0, 
                                  'gpeak_NMDA':0.1,'tau1_NMDA': 4,'tau2_NMDA': 40, 'e_NMDA': 0, 'wratio': wratio[9]} #excitatory synaptic mechanism

# netParams.synMechParams['inL23E'] = netParams.synMechParams['E']
# netParams.synMechParams['inL23E']['wratio'] = wratio[10]

netParams.synMechParams['inL23E'] = {'mod': 'Exc_esser','gpeak_AMPA':0.1, 'tau_m': 1,'tau1_AMPA': 0.5,'tau2_AMPA': 2.4, 'e_AMPA': 0, 
                                  'gpeak_NMDA':0.1,'tau1_NMDA': 4,'tau2_NMDA': 40, 'e_NMDA': 0, 'wratio': wratio[10]} #excitatory synaptic mechanism

# netParams.synMechParams['inInhE'] = netParams.synMechParams['E']
# netParams.synMechParams['inInhE']['wratio'] = wratio[11]

netParams.synMechParams['inInhE'] = {'mod': 'Exc_esser','gpeak_AMPA':0.1, 'tau_m': 1,'tau1_AMPA': 0.5,'tau2_AMPA': 2.4, 'e_AMPA': 0, 
                                  'gpeak_NMDA':0.1,'tau1_NMDA': 4,'tau2_NMDA': 40, 'e_NMDA': 0, 'wratio': wratio[11]} #excitatory synaptic mechanism



# TMS modelled as IClamp at 300 ms
# load cell list activated by TMS
stimint = '50'
with open('L23_cellind_stim_{}.data'.format(stimint), 'rb') as filehandle:
    # read the data as binary data stream
    L23list = pickle.load(filehandle)
with open('L5_cellind_stim_{}.data'.format(stimint), 'rb') as filehandle:
    # read the data as binary data stream
    L5list = pickle.load(filehandle)    
with open('Inh_cellind_stim_{}.data'.format(stimint), 'rb') as filehandle:
    # read the data as binary data stream
    Inhlist = pickle.load(filehandle)   
    
# netParams.stimSourceParams['Iinj1'] = {'type':'IClamp','del':200,'dur':0.2,'amp':5000}
# netParams.stimTargetParams['Iinj1->L23'] = {'source': 'Iinj1', 'sec':'soma', 'loc': 0.5, 'conds': {'pop':'L23exc', 'cellList': L23list}}
# # netParams.stimTargetParams['Iinj1->L23'] = {'source': 'Iinj1', 'sec':'soma', 'loc': 0.5, 'conds': {'pop':'L23exc', 'cellList': range(8)}}

# netParams.stimSourceParams['Iinj2'] = {'type':'IClamp','del':200,'dur':0.2,'amp':5000}
# netParams.stimTargetParams['Iinj2->L5'] = {'source': 'Iinj2', 'sec':'soma', 'loc': 0.5, 'conds': {'pop':'L5exc', 'cellList': L5list}}


# netParams.stimSourceParams['Iinj3'] = {'type':'IClamp','del':200,'dur':0.2,'amp':5000}
# netParams.stimTargetParams['Iinj3->Inh'] = {'source': 'Iinj3', 'sec':'soma', 'loc': 0.5, 'conds': {'pop':'Inh', 'cellList': Inhlist}}

# netParams.stimSourceParams['Input_4'] = {'type': 'NetStim', 'interval': 'uniform(20,100)', 'number': 1000, 'start': 600, 'noise': 0.1}
# netParams.stimTargetParams['Input_4->L23'] = {'source': 'Input_4', 'sec':'soma', 'loc': 0.5, 'weight': '0.1+normal(0.2,0.05)','delay': 1, 'conds': {'pop':'L23exc'}}


# Cell connectivity rules
for i in range(len(df)):
    netParams.connParams['{celltype}{syntype}->{postcell}'.format(celltype = pre_name[i],syntype = syn_type[i], postcell = post_name[i])] = {
     	'preConds': {'pop': '{}'.format(pre_name[i])}, 'postConds': {'pop': '{}'.format(post_name[i])},  
     	'probability': p[i], 		# probability of connection
     	'weight': strength[i], 			# synaptic weight 
     	'delay': 'normal({},{}**2)'.format(delay_mean[i],delay_std[i]),	 	# transmission delay (ms) 
     	'sec': 'soma',				# section to connect to
     	'loc': 0.5,
     	'synMech': '{}'.format(syn_type[i])}   		# target synapse 
    if 'inL5' in pre_name[i]:
        netParams.connParams['{celltype}{syntype}->{postcell}'.format(celltype = pre_name[i],syntype = syn_type[i], postcell = post_name[i])]['synMech'] = 'inL5E'
    if 'inL23' in pre_name[i]:
        netParams.connParams['{celltype}{syntype}->{postcell}'.format(celltype = pre_name[i],syntype = syn_type[i], postcell = post_name[i])]['synMech'] = 'inL23E'
    if 'inInh' in pre_name[i]:
        netParams.connParams['{celltype}{syntype}->{postcell}'.format(celltype = pre_name[i],syntype = syn_type[i], postcell = post_name[i])]['synMech'] = 'inInhE'
    
# TMS modelled as Netstim 
# activate 50% of all population with 1ms delay at 300ms 
# stim_int = 0.1 #perctenage of cells activate 
# netParams.popParams['TMS'] = {'cellModel': 'NetStim', 'interval': 1000, 'noise': 0, 'numCells': 1,'start': 200}  # NetsStim
# netParams.connParams['TMS->all'] = {
#  	'preConds': {'pop': 'TMS'}, 'postConds': {'pop': ['L23exc','L5exc','Inh']},  
#  	'probability': stim_int, 		# probability of connection
#  	'weight': 15, 			# synaptic weight 
#  	'delay': 0.5,					# transmission delay (ms) 
#  	'sec': 'soma',				# section to connect to
#  	'loc': 0.5,
#  	'synMech': 'AMPA'}   		# target synapse 
        


#Simulation options  
simConfig = specs.SimConfig()      # object of class SimConfig to store simulation config
simConfig.duration = 300         # Duration of the simulation, in ms
simConfig.dt = 0.001                       # Internal integration timestep to use
simConfig.verbose = False                   # Show detailed messages 
#simConfig.recordTraces = {'V_soma': {'sec':'soma','loc':0.5, 'var' :'v'}} # Dict with traces to record
#simConfig.recordTraces['gAMPA'] = {'sec':'soma', 'loc':0.5, 'synMech': 'AMPA', 'var': 'g'} # record conductance
#simConfig.recordTraces['gNMDA'] = {'sec':'soma', 'loc':0.5, 'synMech': 'NMDA', 'var': 'g'}
#simConfig.recordTraces['gGABAA'] = {'sec':'soma', 'loc':0.5, 'synMech': 'GABAA', 'var': 'g'}
#simConfig.recordTraces['gGABAB'] = {'sec':'soma', 'loc':0.5, 'synMech': 'GABAB', 'var': 'g'}
# simConfig.recordTraces = {'sec':'soma', 'loc':0.5, 'synMech': 'AMPA', 'var': 'g'}

simConfig.recordStep = 0.01                  # Step size in ms
simConfig.recordStim = True
#sinConfig.saveDataInclude = ['simData']
simConfig.saveFolder = ''
simConfig.saveTxt = True
#simConfig.filename = '' # file output name
simConfig.analysis['plot2Dnet'] = False

sim.initialize(                       # create network object and set cfg and net params
    simConfig = simConfig,   # pass simulation config and network params as arguments
    netParams = netParams)
sim.net.createPops()                      # instantiate network populations
sim.net.createCells()                     # instantiate network cells based on defined populations
sim.net.connectCells()                    # create connections between cells based on params

# % synaptic activation of certain percentage of neuron population (use NetCon.event)
# numL23 = 100
# numL5 = 100
# numInh = 50

# for j in range (len(L23list)):
#     ind = L23list[j]
#     for k in range (len(sim.net.cells[ind].conns)):
#         sim.net.cells[ind].conns[k]['hObj'].event(200)
        
# %% feed cell type to get indices 
celltags = []    
for m in range (len(sim.net.cells)):
    tag = sim.net.cells[m].tags['pop']
    celltags.append(tag)
celltype = 'Inh'
index = cell2ind(celltype,celltags)    
# %%  run simulation
sim.setupRecording()                  # setup variables to record for each cell (spikes, V traces, etc)
sim.runSim()                          # run parallel Neuron simulation
sim.gatherData()                      # gather spiking data and cell info from each node
sim.saveData()                        # save params, cell info and sim output to file (pickle,mat,txt,etc)
sim.analysis.plotData()                   # plot spike raster


# Create network and run simulation
# sim.createSimulateAnalyze(netParams = netParams, simConfig = simConfig)


#%% Save raster for each population
TMSpop = 'TMSall' # population activated by TMS
Stimint = 'stim10' # stim intensity
# sim.analysis.plotRaster(include=[('L23exc'),('inL23exc')],spikeHist='overlay',spikeHistBin = 10,saveData = 'raster_{}_{}_single_L23.pkl'.format(TMSpop,Stimint))
# sim.analysis.plotRaster(include=[('L5exc'),('inL5exc')],spikeHist='overlay',spikeHistBin = 10,saveData = 'raster_{}_{}_single_L5.pkl'.format(TMSpop,Stimint))
# sim.analysis.plotRaster(include=[('Inh'),('inInh')],spikeHist='overlay',spikeHistBin = 10,saveData = 'raster_{}_{}_single_Inh.pkl'.format(TMSpop,Stimint))
#sim.analysis.plotTraces(include = [('L23exc'),('L5exc'),('Inh')],saveData = 'gsyn_TMS.pkl')
sim.analysis.plotRaster(include=[('L23exc'),('inL23exc')],spikeHist='overlay',spikeHistBin = 10)
sim.analysis.plotRaster(include=[('L5exc'),('inL5exc')],spikeHist='overlay',spikeHistBin = 10)
sim.analysis.plotRaster(include=[('Inh'),('inInh')],spikeHist='overlay',spikeHistBin = 10)

# save raster (combine synapse)
sim.analysis.plotRaster(include=[('L23exc'),('inL23exc')],spikeHist='overlay',spikeHistBin = 10,saveData = 'raster_{}_{}_single_L23_old.pkl'.format(TMSpop,Stimint))
sim.analysis.plotRaster(include=[('L5exc'),('inL5exc')],spikeHist='overlay',spikeHistBin = 10,saveData = 'raster_{}_{}_single_L5_old.pkl'.format(TMSpop,Stimint))
sim.analysis.plotRaster(include=[('Inh'),('inInh')],spikeHist='overlay',spikeHistBin = 10,saveData = 'raster_{}_{}_single_Inh_old.pkl'.format(TMSpop,Stimint))
