# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 15:50:08 2020

@author: zhaoz
"""
# %%
import numpy as np
from netpyne import specs, sim

#Network parameters
netParams = specs.NetParams() # object of class NetParams to store the network parameters

#Create three neuron population :L23exc, L5exc and Inh
netParams.popParams['L23exc'] = {'cellType': 'L23exc', 'numCells': 100, 'cellModel': 'L23exc_esser'}
netParams.popParams['L5exc'] = {'cellType':'L5exc','numCells':100, 'cellModel': 'L5exc_esser'}
netParams.popParams['Inh'] = {'cellType': 'Inh', 'numCells': 50, 'cellModel': 'Inh_esser'}

#Create poisson input population 
netParams.popParams['inL23exc'] = {'cellModel': 'NetStim', 'interval': 1000/8, 'noise': 1, 'numCells': 100,'start': 0}  # NetsStim
netParams.popParams['inL5exc'] = {'cellModel': 'NetStim', 'interval': 1000/10, 'noise': 1, 'numCells': 100,'start': 0}  # NetsStim
netParams.popParams['inInh'] = {'cellModel': 'NetStim', 'interval': 1000/16, 'noise': 1, 'numCells': 100,'start': 0}  # NetsStim


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

cellRule = {'conds': {'cellType': 'Inh', 'cellModel': 'Inh_esser'},  'secs': {}} 						# cell rule dict
cellRule['secs']['soma'] = {'geom': {}, 'ions':{}, 'pointps': {}, 'vinit':{}}  												# soma params dict
cellRule['secs']['soma']['geom'] = {'diam':1500, 'L': 18.8, 'Ra':123.0,'cm':7}
cellRule['secs']['soma']['pointps']['esser'] = {'mod':'esser_mech', 
              'theta_eq' : -54,'tau_theta' : 1,'tau_spike' : 0.48/7,'tau_m' : 7/7,'gNa_leak' : 0.2,
              'gK_leak' : 1.0, 'tspike' : 0.75}  					# soma hh mechanisms
cellRule['secs']['soma']['ions'] = {'na':{'e':30.0},'k':{'e':-90}}
cellRule['secs']['soma']['vinit'] = -75.263
netParams.cellParams['Inh_rule'] = cellRule


# Synaptic mechanism parameters
netParams.synMechParams['AMPA'] = {'mod': 'Exp2Syn_esser','gpeak':0.1, 'tau_m': 1,'tau1': 0.5,'tau2': 2.4, 'e': 0} #excitatory synaptic mechanism
netParams.synMechParams['NMDA'] = {'mod': 'NMDA_esser','gpeak':0.1, 'tau_m': 1,'tau1': 4,'tau2': 40, 'e': 0} #excitatory synaptic mechanism
netParams.synMechParams['GABAA'] = {'mod': 'Exp2Syn_esser','gpeak':0.33, 'tau_m': 1,'tau1': 1,'tau2': 7, 'e': -70} #Inhibitory synaptic mechanism
netParams.synMechParams['GABAB'] = {'mod': 'Exp2Syn_esser','gpeak':0.0132, 'tau_m': 1,'tau1': 60,'tau2': 200, 'e': -90} #inhibitory synaptic mechanism

# Cell connectivity rules
netParams.connParams['inL23AMPA->L23'] = {
	'preConds': {'pop': 'inL23exc'}, 'postConds': {'pop': 'L23exc'},  
	'probability': 0.15, 		# probability of connection
	'weight': 2.7, 			# synaptic weight 
	'delay': 'normal(6,0.25)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'AMPA'}   		# target synapse 

netParams.connParams['inL23NMDA->L23'] = {
	'preConds': {'pop': 'inL23exc'}, 'postConds': {'pop': 'L23exc'},  
	'probability': 0.15, 		# probability of connection
	'weight': 0.1, 			# synaptic weight 
	'delay': 'normal(6,0.25)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'NMDA'}   		# target synapse 

netParams.connParams['inL5AMPA->L5'] = {
	'preConds': {'pop': 'inL5exc'}, 'postConds': {'pop': 'L5exc'},  
	'probability': 0.15, 		# probability of connection
	'weight': 4.5, 			# synaptic weight 
	'delay': 'normal(6,0.25)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'AMPA'}   		# target synapse 

netParams.connParams['inL5NMDA->L5'] = {
	'preConds': {'pop': 'inL5exc'}, 'postConds': {'pop': 'L5exc'},  
	'probability': 0.15, 		# probability of connection
	'weight': 0.1, 			# synaptic weight 
	'delay': 'normal(6,0.25)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'NMDA'}   		# target synapse 

netParams.connParams['inInhAMPA->Inh'] = {
	'preConds': {'pop': 'inInh'}, 'postConds': {'pop': 'Inh'},  
	'probability': 0.15, 		# probability of connection
	'weight': 2, 			# synaptic weight 
	'delay': 'normal(6,0.25)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'AMPA'}   		# target synapse 

netParams.connParams['inInhNMDA->Inh'] = {
	'preConds': {'pop': 'inInh'}, 'postConds': {'pop': 'Inh'},  
	'probability': 0.15, 		# probability of connection
	'weight': 0.8, 			# synaptic weight 
	'delay': 'normal(6,0.25)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'NMDA'}   		# target synapse 


# L23 connection to other population
netParams.connParams['L23AMPA->L23'] = {
	'preConds': {'pop': 'L23exc'}, 'postConds': {'pop': 'L23exc'},  
	'probability': 0.05, 		# probability of connection
	'weight': 1, 			# synaptic weight 
	'delay': 'normal(0.4,0.01)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'AMPA'}   		# target synapse 

netParams.connParams['L23NMDA->L23'] = {
	'preConds': {'pop': 'L23exc'}, 'postConds': {'pop': 'L23exc'},  
	'probability': 0.05, 		# probability of connection
	'weight': 0.1, 			# synaptic weight 
	'delay': 'normal(0.4,0.01)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'NMDA'}   		# target synapse 

netParams.connParams['L23AMPA->L5'] = {
	'preConds': {'pop': 'L23exc'}, 'postConds': {'pop': 'L5exc'},  
	'probability': 0.06, 		# probability of connection
	'weight': 1, 			# synaptic weight 
	'delay': 'normal(1.4,0.0625)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'AMPA'}   		# target synapse 

netParams.connParams['L23NMDA->L5'] = {
	'preConds': {'pop': 'L23exc'}, 'postConds': {'pop': 'L5exc'},  
	'probability': 0.06, 		# probability of connection
	'weight': 0.1, 			# synaptic weight 
	'delay': 'normal(1.4,0.0625)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'NMDA'}   		# target synapse 

netParams.connParams['L23AMPA->Inh'] = {
	'preConds': {'pop': 'L23exc'}, 'postConds': {'pop': 'Inh'},  
	'probability': 0.09, 		# probability of connection
	'weight': 1.75, 			# synaptic weight 
	'delay': 'normal(0.4,0.01)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'AMPA'}   		# target synapse 

netParams.connParams['L23NMDA->Inh'] = {
	'preConds': {'pop': 'L23exc'}, 'postConds': {'pop': 'Inh'},  
	'probability': 0.09, 		# probability of connection
	'weight': 0.175, 			# synaptic weight 
	'delay': 'normal(0.4,0.01)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'NMDA'}   		# target synapse 
   
#L5 connection to other population
netParams.connParams['L5AMPA->L23'] = {
	'preConds': {'pop': 'L5exc'}, 'postConds': {'pop': 'L23exc'},  
	'probability': 0.01, 		# probability of connection
	'weight': 1, 			# synaptic weight 
	'delay': 'normal(1.4,0.0625)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'AMPA'}   		# target synapse 

netParams.connParams['L5NMDA->L23'] = {
	'preConds': {'pop': 'L5exc'}, 'postConds': {'pop': 'L23exc'},  
	'probability': 0.01, 		# probability of connection
	'weight': 0.1, 			# synaptic weight 
	'delay': 'normal(1.4,0.0625)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'NMDA'}   		# target synapse 

netParams.connParams['L5AMPA->L5'] = {
	'preConds': {'pop': 'L5exc'}, 'postConds': {'pop': 'L5exc'},  
	'probability': 0.0625, 		# probability of connection
	'weight': 1, 			# synaptic weight 
	'delay': 'normal(1.4,0.0625)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'AMPA'}   		# target synapse 

netParams.connParams['L5NMDA->L5'] = {
	'preConds': {'pop': 'L5exc'}, 'postConds': {'pop': 'L5exc'},  
	'probability': 0.0625, 		# probability of connection
	'weight': 0.1, 			# synaptic weight 
	'delay': 'normal(1.4,0.0625)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'NMDA'}   		# target synapse

netParams.connParams['L5AMPA->Inh'] = {
	'preConds': {'pop': 'L5exc'}, 'postConds': {'pop': 'Inh'},  
	'probability': 0.025, 		# probability of connection
	'weight': 1.75, 			# synaptic weight 
	'delay': 'normal(0.4,0.01)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'AMPA'}   		# target synapse

netParams.connParams['L5NMDA->Inh'] = {
	'preConds': {'pop': 'L5exc'}, 'postConds': {'pop': 'Inh'},  
	'probability': 0.025, 		# probability of connection
	'weight': 0.175, 			# synaptic weight 
	'delay': 'normal(0.4,0.01)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'NMDA'}   		# target synapse

#Inh connection to other population 
netParams.connParams['InhGA->L23'] = {
	'preConds': {'pop': 'Inh'}, 'postConds': {'pop': 'L23exc'},  
	'probability': 0.12, 		# probability of connection
	'weight': 1, 			# synaptic weight 
	'delay': 'normal(0.4,0.01)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'GABAA'}   		# target synapse

netParams.connParams['InhGB->L23'] = {
	'preConds': {'pop': 'Inh'}, 'postConds': {'pop': 'L23exc'},  
	'probability': 0.12, 		# probability of connection
	'weight': 2.777, 			# synaptic weight 
	'delay': 'normal(0.4,0.01)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'GABAB'}   		# target synapse

netParams.connParams['InhGA->L5'] = {
	'preConds': {'pop': 'Inh'}, 'postConds': {'pop': 'L5exc'},  
	'probability': 0.15, 		# probability of connection
	'weight': 0.75, 			# synaptic weight 
	'delay': 'normal(0.4,0.01)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'GABAA'}   		# target synapse

netParams.connParams['InhGB->L5'] = {
	'preConds': {'pop': 'Inh'}, 'postConds': {'pop': 'L5exc'},  
	'probability': 0.15, 		# probability of connection
	'weight': 1.3885, 			# synaptic weight 
	'delay': 'normal(0.4,0.01)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'GABAB'}   		# target synapse

netParams.connParams['InhGA->Inh'] = {
	'preConds': {'pop': 'Inh'}, 'postConds': {'pop': 'Inh'},  
	'probability': 0.15, 		# probability of connection
	'weight': 1, 			# synaptic weight 
	'delay': 'normal(0.4,0.01)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'GABAA'}   		# target synapse

netParams.connParams['InhGB->Inh'] = {
	'preConds': {'pop': 'Inh'}, 'postConds': {'pop': 'Inh'},  
	'probability': 0.15, 		# probability of connection
	'weight': 2.777, 			# synaptic weight 
	'delay': 'normal(0.4,0.01)',					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'GABAB'}   		# target synapse


#netParams.stimSourceParams['Input_1'] = {'type': 'IClamp', 'del': 0, 'dur': 1000, 'amp': 26}
#netParams.stimTargetParams['Input_1->L23exc'] = {'source': 'Input_1', 'sec':'soma', 'loc': 0.5, 'conds': {'cellType':'L23exc'}}
#
#netParams.stimSourceParams['Input_2'] = {'type': 'IClamp', 'del': 0, 'dur': 1000, 'amp': 37}
#netParams.stimTargetParams['Input_2->L5exc'] = {'source': 'Input_2', 'sec':'soma', 'loc': 0.5, 'conds': {'cellType':'L5exc'}}
#
#netParams.stimSourceParams['Input_3'] = {'type': 'IClamp', 'del': 0, 'dur': 200, 'amp': 19}
#netParams.stimTargetParams['Input_3->Inh'] = {'source': 'Input_3', 'sec':'soma', 'loc': 0.5, 'conds': {'cellType':'Inh'}}


#Simulation options  
simConfig = specs.SimConfig()      # object of class SimConfig to store simulation config
simConfig.duration = 1000         # Duration of the simulation, in ms
simConfig.dt = 0.001                       # Internal integration timestep to use
simConfig.verbose = False                   # Show detailed messages 
simConfig.recordTraces = {'V_soma': {'sec':'soma','loc':0.5, 'var' :'v'}} # Dict with traces to record
simConfig.recordTraces['gAMPA'] = {'sec':'soma', 'loc':0.5, 'synMech': 'AMPA', 'var': 'g'}
simConfig.recordTraces['gNMDA'] = {'sec':'soma', 'loc':0.5, 'synMech': 'NMDA', 'var': 'g'}
simConfig.recordTraces['gGABAA'] = {'sec':'soma', 'loc':0.5, 'synMech': 'GABAA', 'var': 'g'}
simConfig.recordTraces['gGABAB'] = {'sec':'soma', 'loc':0.5, 'synMech': 'GABAB', 'var': 'g'}

simConfig.recordStep = 0.01                  # Step size in ms
simConfig.recordStim = True
#sinConfig.saveDataInclude = ['simData']
simConfig.saveFolder = 'D:\School work\TMS\nhp_tms_microcircuit\netpyne\dataset'
simConfig.saveTxt = True
simConfig.filename = 'raster2_spon_inon_Inh' # file output name
#simConfig.savePickle = False           #Save params, network and sim output to pickle file

#simConfig.analysis['plotRaster'] = True
#simConfig.analysis['plotRaster'] = {'include':[('inInh'),('Inh')],'spikeHist':'overlay','spikeHistBin': 5,'saveData': True}
#simConfig.analysis['plotTraces'] = {'include':[('L23exc',0),('L5exc',0),('Inh',0)],'overlay':False,'oneFigPer':'trace'}
#simConfig.analysis['plotTraces'] = {'include':[('L23exc',0),('L5exc',0),('Inh',0)]}
simConfig.analysis['plot2Dnet'] = False

sim.initialize(                       # create network object and set cfg and net params
    simConfig = simConfig,   # pass simulation config and network params as arguments
    netParams = netParams)
sim.net.createPops()                      # instantiate network populations
sim.net.createCells()                     # instantiate network cells based on defined populations
sim.net.connectCells()                    # create connections between cells based on params

#Poisson firing rate for each poisson inputs 
frinh = np.random.normal(16,0,100) #FRmean 16 Hz 
frl23 = np.random.normal(8,0,100)#FRmean 8 Hz
frl5 = np.random.normal(10,0,100) #FRmean 10 Hz
i=0; j=0;k=0;
for x in range (0,len(sim.net.cells)-1):
    if 'inInh' in sim.net.cells[x].tags['pop']:
        sim.net.cells[x].params['interval'] = 1000/frinh[i]
        i+=1
    if 'inL23exc' in sim.net.cells[x].tags['pop']:
        sim.net.cells[x].params['interval'] = 1000/frl23[j]
        j+=1
    if 'inL5exc' in sim.net.cells[x].tags['pop']:
        sim.net.cells[x].params['interval'] = 1000/frl5[k]
        k+=1
# %%
sim.setupRecording()                  # setup variables to record for each cell (spikes, V traces, etc)
sim.runSim()                          # run parallel Neuron simulation
sim.gatherData()                      # gather spiking data and cell info from each node
sim.saveData()                        # save params, cell info and sim output to file (pickle,mat,txt,etc)
sim.analysis.plotData()                   # plot spike raster
#%% Save raster for each population
sim.analysis.plotRaster(include=[('L23exc'),('inL23exc')],spikeHist='overlay',spikeHistBin = 10,saveData = 'raster5_spon_inon_L23.pkl')
sim.analysis.plotRaster(include=[('L5exc'),('inL5exc')],spikeHist='overlay',spikeHistBin = 10,saveData = 'raster5_spon_inon_L5.pkl')
sim.analysis.plotRaster(include=[('Inh'),('inInh')],spikeHist='overlay',spikeHistBin = 10,saveData = 'raster5_spon_inon_Inh.pkl')
sim.analysis.plotTraces(include = 'all',saveData = 'gsyn4.pkl')