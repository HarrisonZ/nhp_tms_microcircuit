# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 19:11:19 2020

@author: zhaoz
"""

from netpyne import specs, sim

#Network parameters
netParams = specs.NetParams() # object of class NetParams to store the network parameters

#Create three neuron population :L23exc, L5exc and Inh
netParams.popParams['L23exc'] = {'cellType': 'L23exc', 'numCells': 1, 'cellModel': 'L23exc_esser'}
netParams.popParams['L5exc'] = {'cellType':'L5exc','numCells':1, 'cellModel': 'L5exc_esser'}
netParams.popParams['Inh'] = {'cellType': 'Inh', 'numCells': 1, 'cellModel': 'Inh_esser'}

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
cellRule['secs']['soma']['vinit'] = -75.263
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
netParams.synMechParams['AMPA'] = {'mod': 'Exp2Syn_esser','gpeak':0.1, 'tau_m': 13/13,'tau1': 0.5,'tau2': 2.4, 'e': 0} #excitatory synaptic mechanism
netParams.synMechParams['NMDA'] = {'mod': 'NMDA_esser','gpeak':1, 'tau_m': 13/13,'tau1': 4,'tau2': 40, 'e': 0} #excitatory synaptic mechanism
netParams.synMechParams['GABAA'] = {'mod': 'Exp2Syn_esser','gpeak':0.33, 'tau_m': 1,'tau1': 1,'tau2': 7, 'e': -70} #Inhibitory synaptic mechanism
netParams.synMechParams['GABAB'] = {'mod': 'Exp2Syn_esser','gpeak':0.0132, 'tau_m': 13/13,'tau1': 60,'tau2': 200, 'e': -90} #inhibitory synaptic mechanism

#stimulation
#netParams.stimSourceParams['bkg'] = {'type': 'NetStim','rate': 10, 'noise': 0.5}
# stim connects to the cells
#netParams.stimTargetParams['bkg->L23Exc'] = {'source': 'bkg', 'conds': {'cellType': 'L23Exc'}, 'weight': 1, 'delay': 2, 'synMech': 'exc'}
# Cell connectivity rules
netParams.connParams['L23->L5'] = {
	'preConds': {'pop': 'L23exc'}, 'postConds': {'pop': 'L5exc'},  
	'probability': 1, 		# probability of connection
	'weight': 2, 			# synaptic weight 
	'delay': 0,					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'NMDA'}   		# target synapse 

netParams.connParams['L23->Inh'] = {
	'preConds': {'pop': 'L23exc'}, 'postConds': {'pop': 'Inh'},  
	'probability': 1, 		# probability of connection
	'weight': 1.5, 			# synaptic weight 
	'delay': 0,					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'AMPA'}   		# target synapse 

netParams.connParams['L5->Inh'] = {
	'preConds': {'pop': 'L5exc'}, 'postConds': {'pop': 'Inh'},  
	'probability': 1, 		# probability of connection
	'weight': 1.75, 			# synaptic weight 
	'delay': 0,					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'AMPA'}   		# target synapse 

netParams.connParams['Inh->L5'] = {
	'preConds': {'pop': 'Inh'}, 'postConds': {'pop': 'L5exc'},  
	'probability': 1, 		# probability of connection
	'weight': 2, 			# synaptic weight 
	'delay': 0,					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'GABAB'}   		# target synapse 

netParams.connParams['Inh->L23'] = {
	'preConds': {'pop': 'Inh'}, 'postConds': {'pop': 'L23exc'},  
	'probability': 1, 		# probability of connection
	'weight': 2.5, 			# synaptic weight 
	'delay': 0,					# transmission delay (ms) 
	'sec': 'soma',				# section to connect to
	'loc': 0.5,
	'synMech': 'GABAA'}   		# target synapse 


netParams.stimSourceParams['Input_1'] = {'type': 'IClamp', 'del': 0, 'dur': 1000, 'amp': 26}
netParams.stimTargetParams['Input_1->L23exc'] = {'source': 'Input_1', 'sec':'soma', 'loc': 0.5, 'conds': {'cellType':'L23exc'}}

#netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': 1, 'noise': 0}
#netParams.stimTargetParams['bkg->PYR'] = {'source': 'bkg', 'conds': {'cellType': ['L5exc']}, 'weight': 1, 'delay': 100, 'synMech': 'NMDA'}

#netParams.stimSourceParams['Input_2'] = {'type': 'IClamp', 'del': 0, 'dur': 1000, 'amp': 37}
#netParams.stimTargetParams['Input_2->L5exc'] = {'source': 'Input_2', 'sec':'soma', 'loc': 0.5, 'conds': {'cellType':'L5exc'}}

#netParams.stimSourceParams['Input_3'] = {'type': 'IClamp', 'del': 0, 'dur': 200, 'amp': 19}
#netParams.stimTargetParams['Input_3->Inh'] = {'source': 'Input_3', 'sec':'soma', 'loc': 0.5, 'conds': {'cellType':'Inh'}}


#Simulation options  
simConfig = specs.SimConfig()      # object of class SimConfig to store simulation config
simConfig.duration = 300         # Duration of the simulation, in ms
simConfig.dt = 0.001                       # Internal integration timestep to use
simConfig.verbose = False                   # Show detailed messages 
simConfig.recordTraces = {'V_soma': {'sec':'soma','loc':0.5, 'var' :'v'}} # Dict with traces to record
simConfig.recordStep = 0.01                  # Step size in ms
simConfig.recordStim = True
simConfig.saveTxt = True
simConfig.filename = 'model_output' # file output name
simConfig.savePickle = False           #Save params, network and sim output to pickle file

simConfig.analysis['plotRaster'] = False
simConfig.analysis['plotTraces'] = {'include':[('L23exc',0),('L5exc',0),('Inh',0)],'overlay':False,'oneFigPer':'trace'}
simConfig.analysis['plot2Dnet'] = False

sim.createSimulateAnalyze(netParams, simConfig)