# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 13:45:01 2020

@author: zhaoz
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 09:14:16 2020

@author: zhaoz
"""

from netpyne import specs, sim
from loadfile import df
import os
import inspect
# get file direction 
fn = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(fn))
data_fold = 'dataset'
datadir = os.path.join(path,data_fold)
#Network parameters
netParams = specs.NetParams() # object of class NetParams to store the network parameters

#Create three neuron population :L23exc, L5exc and Inh
netParams.popParams['L23exc'] = {'cellType': 'L23exc', 'numCells': 100, 'cellModel': 'L23exc_esser'}
netParams.popParams['L5exc'] = {'cellType':'L5exc','numCells':100, 'cellModel': 'L5exc_esser'}
netParams.popParams['Inh'] = {'cellType': 'Inh', 'numCells': 50, 'cellModel': 'Inhb_esser'}

#Create poisson input population 
#netParams.popParams['inL23exc'] = {'cellModel': 'NetStim', 'rate': '0 + normal(6.0,1.0)', 'noise': 0, 'numCells': 20,'start': 0}  # NetsStim
#netParams.popParams['inL5exc'] = {'cellModel': 'NetStim', 'rate': '0 + normal(6.0,1.0)', 'noise': 0, 'numCells': 20,'start': 0}  # NetsStim
#netParams.popParams['inInh'] = {'cellModel': 'NetStim', 'rate': '0 + normal(14.0,4.0)', 'noise': 0, 'numCells': 20,'start': 0}  # NetsStim
netParams.popParams['inL23exc'] = {'cellModel': 'NetStim', 'interval': 1000/8, 'noise': 1, 'numCells': 100,'start': 0}  # NetsStim
netParams.popParams['inL5exc'] = {'cellModel': 'NetStim', 'interval': 1000/10, 'noise': 1, 'numCells': 100,'start': 0}  # NetsStim
netParams.popParams['inInh'] = {'cellModel': 'NetStim', 'interval': 1000/16, 'noise': 1, 'numCells': 100,'start': 0}  # NetsStim
#netParams.popParams['inL23exc'] = {'cellModel': 'NetStim', 'interval': 'normal(125,64)', 'noise': 0.1, 'numCells': 10,'start': 0}  # NetsStim
#netParams.popParams['inL5exc'] = {'cellModel': 'NetStim', 'interval': 'normal(100,49)', 'noise': 0.1, 'numCells': 10,'start': 0}  # NetsStim
#netParams.popParams['inInh'] = {'cellModel': 'NetStim', 'interval': 'normal(62.5,16)', 'noise': 0.1, 'numCells': 10,'start': 0}  # NetsStim


cellRule = {'conds': {'cellType': 'L23exc', 'cellModel': 'L23exc_esser'},  'secs': {}} 						# cell rule dict
cellRule['secs']['soma'] = {'geom': {}, 'ions':{}, 'pointps': {}, 'vinit':{}}  												# soma params dict
cellRule['secs']['soma']['geom'] = {'diam':1500, 'L': 18.8, 'Ra':123.0,'cm':15}
cellRule['secs']['soma']['pointps']['esser'] = {'mod':'esser_mech', 
              'theta_eq' : -53,'tau_theta' : 2,'tau_spike' : 1.75/15,'tau_m' : 15/15,'gNa_leak' : 0.14,
              'gK_leak' : 1.0, 'tspike' : 2.0}  					# soma hh mechanisms
cellRule['secs']['soma']['ions'] = {'na':{'e':30.0},'k':{'e':-90}}
cellRule['secs']['soma']['vinit'] = -75.263
netParams.cellParams['L23exc_esser_rule'] = cellRule

cellRule = {'conds': {'cellType': 'L5exc', 'cellModel': 'L5exc_esser'},  'secs': {}} 						# cell rule dict
cellRule['secs']['soma'] = {'geom': {}, 'ions':{}, 'pointps': {}, 'vinit':{}}  												# soma params dict
cellRule['secs']['soma']['geom'] = {'diam':1500, 'L':18.8, 'Ra':123.0,'cm':13}
cellRule['secs']['soma']['pointps']['esser'] = {'mod':'esser_mech', 
              'theta_eq' : -53,'tau_theta' : 0.5,'tau_spike' : 0.6/13,'tau_m' : 13/13,'gNa_leak' : 0.14,
              'gK_leak' : 1.3, 'tspike' : 0.75}  					# soma hh mechanisms
cellRule['secs']['soma']['ions'] = {'na':{'e':30.0},'k':{'e':-90}}
cellRule['secs']['soma']['vinit'] = -78.33
netParams.cellParams['L5exc_esser_rule'] = cellRule 			# add dict to list of cell parameters

cellRule = {'conds': {'cellType': 'Inh', 'cellModel': 'Inhb_esser'},  'secs': {}} 						# cell rule dict
cellRule['secs']['soma'] = {'geom': {}, 'ions':{}, 'pointps': {}, 'vinit':{}}  												# soma params dict
cellRule['secs']['soma']['geom'] = {'diam':1500, 'L': 18.8, 'Ra':123.0,'cm':7}
cellRule['secs']['soma']['pointps']['esser'] = {'mod':'esser_mech', 
              'theta_eq' : -54,'tau_theta' : 1,'tau_spike' : 0.48/7,'tau_m' : 7/7,'gNa_leak' : 0.2,
              'gK_leak' : 1.0, 'tspike' : 0.75}  					# soma hh mechanisms
cellRule['secs']['soma']['ions'] = {'na':{'e':30.0},'k':{'e':-90}}
cellRule['secs']['soma']['vinit'] = -75.263
netParams.cellParams['Inh_rule'] = cellRule


# Synaptic mechanism parameters
# netParams.synMechParams['AMPA'] = {'mod': 'Exp2Syn_esser','gpeak':0.1, 'tau_m': 13/13,'tau1': 0.5,'tau2': 2.4, 'e': 0} #excitatory synaptic mechanism
# netParams.synMechParams['NMDA'] = {'mod': 'NMDA_esser','gpeak':0.1, 'tau_m': 13/13,'tau1': 4,'tau2': 40, 'e': 0} #excitatory synaptic mechanism
# netParams.synMechParams['GABAA'] = {'mod': 'Exp2Syn_esser','gpeak':0.33, 'tau_m': 1,'tau1': 1,'tau2': 7, 'e': -70} #Inhibitory synaptic mechanism
# netParams.synMechParams['GABAB'] = {'mod': 'Exp2Syn_esser','gpeak':0.0132, 'tau_m': 13/13,'tau1': 60,'tau2': 200, 'e': -90} #inhibitory synaptic mechanism

# Read params from excel and create synaptic connections in a loop 
pre_name = df["pre_name"]
post_name = df["post_name"]
syn_type = df["pre_type"]
delay_mean = df["delay_mean"]
delay_std = df["delay_std"]
strength = df["strength"]
p = df["p"]
wratio = df["wratio"]

netParams.synMechParams['E'] = {'mod': 'Exc_esser','gpeak_AMPA':0.1, 'tau_m': 1,'tau1_AMPA': 0.5,'tau2_AMPA': 2.4, 'e_AMPA': 0, 
                                  'gpeak_NMDA':0.1,'tau1_NMDA': 4,'tau2_NMDA': 40, 'e_NMDA': 0, 'wratio': wratio[1]} #excitatory synaptic mechanism
netParams.synMechParams['I'] = {'mod': 'Inh_esser','gpeak_GABAA':0.33, 'tau_m': 1,'tau1_GABAA': 1,'tau2_GABAA': 7, 'e_GABAA': -70,
                                  'gpeak_GABAB':0.0132, 'tau1_GABAB': 60,'tau2_GABAB': 200, 'e_GABAB': -90 , 'wratio':wratio[8]} #Inhibitory synaptic mechanism
netParams.synMechParams['inL5E'] = {'mod': 'Exc_esser','gpeak_AMPA':0.1, 'tau_m': 1,'tau1_AMPA': 0.5,'tau2_AMPA': 2.4, 'e_AMPA': 0, 
                                  'gpeak_NMDA':0.1,'tau1_NMDA': 4,'tau2_NMDA': 40, 'e_NMDA': 0, 'wratio': wratio[9]} #excitatory synaptic mechanism
netParams.synMechParams['inL23E'] = {'mod': 'Exc_esser','gpeak_AMPA':0.1, 'tau_m': 1,'tau1_AMPA': 0.5,'tau2_AMPA': 2.4, 'e_AMPA': 0, 
                                  'gpeak_NMDA':0.1,'tau1_NMDA': 4,'tau2_NMDA': 40, 'e_NMDA': 0, 'wratio': wratio[10]} #excitatory synaptic mechanism
netParams.synMechParams['inInhE'] = {'mod': 'Exc_esser','gpeak_AMPA':0.1, 'tau_m': 1,'tau1_AMPA': 0.5,'tau2_AMPA': 2.4, 'e_AMPA': 0, 
                                  'gpeak_NMDA':0.1,'tau1_NMDA': 4,'tau2_NMDA': 40, 'e_NMDA': 0, 'wratio': wratio[11]} #excitatory synaptic mechanism

# Cell connectivity rules 
# pre_name = df["pre_name"]
# post_name = df["post_name"]
# syn_name = df["syn_name"]
# delay_mean = df["delay_mean"]
# delay_std = df["delay_std"]
# strength = df["strength"]
# p = df["p"]

# for i in range(len(df)):
#     netParams.connParams['{celltype}{syntype}->{postcell}'.format(celltype = pre_name[i],syntype = syn_name[i], postcell = post_name[i])] = {
#     	'preConds': {'pop': '{}'.format(pre_name[i])}, 'postConds': {'pop': '{}'.format(post_name[i])},  
#     	'probability': p[i], 		# probability of connection
#     	'weight': strength[i], 			# synaptic weight 
#     	'delay': 'normal({},{}**2)'.format(delay_mean[i],delay_std[i]),					# transmission delay (ms) 
#     	'sec': 'soma',				# section to connect to
#     	'loc': 0.5,
#     	'synMech': '{}'.format(syn_name[i])}   		# target synapse 
    


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


#Simulation options  
simConfig = specs.SimConfig()      # object of class SimConfig to store simulation config
simConfig.duration = 1000         # Duration of the simulation, in ms
simConfig.dt = 0.001                       # Internal integration timestep to use
simConfig.verbose = False                   # Show detailed messages 
#simConfig.recordTraces = {'V_soma': {'sec':'soma','loc':0.5, 'var' :'v'}} # Dict with traces to record
#simConfig.recordTraces['gAMPA'] = {'sec':'soma', 'loc':0.5, 'synMech': 'AMPA', 'var': 'g'}
#simConfig.recordTraces['gNMDA'] = {'sec':'soma', 'loc':0.5, 'synMech': 'NMDA', 'var': 'g'}
#simConfig.recordTraces['gGABAA'] = {'sec':'soma', 'loc':0.5, 'synMech': 'GABAA', 'var': 'g'}
#simConfig.recordTraces['gGABAB'] = {'sec':'soma', 'loc':0.5, 'synMech': 'GABAB', 'var': 'g'}
simConfig.recordTraces = {'sec':'soma', 'loc':0.5, 'synMech': 'AMPA', 'var': 'g'}

simConfig.recordStep = 0.01                  # Step size in ms
simConfig.recordStim = True
#sinConfig.saveDataInclude = ['simData']
simConfig.saveFolder = datadir
simConfig.saveTxt = True
#simConfig.filename = 'raster2_spon_inon_Inh' # file output name
simConfig.analysis['plot2Dnet'] = False

sim.initialize(                       # create network object and set cfg and net params
    simConfig = simConfig,   # pass simulation config and network params as arguments
    netParams = netParams)
sim.net.createPops()                      # instantiate network populations
sim.net.createCells()                     # instantiate network cells based on defined populations
sim.net.connectCells()                    # create connections between cells based on params

# %%
sim.setupRecording()                  # setup variables to record for each cell (spikes, V traces, etc)
sim.runSim()                          # run parallel Neuron simulation
sim.gatherData()                      # gather spiking data and cell info from each node
sim.saveData()                        # save params, cell info and sim output to file (pickle,mat,txt,etc)
sim.analysis.plotData()                   # plot spike raster
#%% Save raster for each population
sim.analysis.plotRaster(include=[('L23exc'),('inL23exc')],spikeHist='overlay',spikeHistBin = 10,saveData = 'raster_spon_inon_L23test.pkl')
sim.analysis.plotRaster(include=[('L5exc'),('inL5exc')],spikeHist='overlay',spikeHistBin = 10,saveData = 'raster_spon_inon_L5test.pkl')
sim.analysis.plotRaster(include=[('Inh'),('inInh')],spikeHist='overlay',spikeHistBin = 10,saveData = 'raster_spon_inon_Inhtest.pkl')
# sim.analysis.plotTraces(include = [('L23exc'),('L5exc'),('Inh')],saveData = 'gsyn_TMS.pkl')
# sim.analysis.plotRaster(include=[('L23exc'),('inL23exc')],spikeHist='overlay',spikeHistBin = 10)
# sim.analysis.plotRaster(include=[('L5exc'),('inL5exc')],spikeHist='overlay',spikeHistBin = 10)
# sim.analysis.plotRaster(include=[('Inh'),('inInh')],spikeHist='overlay',spikeHistBin = 10)