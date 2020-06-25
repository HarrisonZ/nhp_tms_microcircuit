# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 16:24:37 2020

@author: zhaoz
"""

from netpyne import specs, sim

#Network parameters
netParams = specs.NetParams() # object of class NetParams to store the network parameters

netParams.popParams['L23exc'] = {'cellType': 'L23exc', 'numCells': 10, 'cellModel': 'L23exc_esser'}
netParams.popParams['L5exc'] = {'cellType':'L5exc','numCells':10, 'cellModel': 'L5exc_esser'}
# netParams.popParams['inh'] = {'cellType': 'inh', 'numCells': 10, 'cellModel': 'inh_esser'}

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

# cellRule = {'conds': {'cellType': 'inh', 'cellModel': 'inh_esser'},  'secs': {}} 						# cell rule dict
# cellRule['secs']['soma'] = {'geom': {}, 'ions':{}, 'pointps': {}, 'vinit':{}}  												# soma params dict
# cellRule['secs']['soma']['geom'] = {'diam':1500, 'L': 18.8, 'Ra':123.0,'cm':7}
# cellRule['secs']['soma']['pointps']['esser'] = {'mod':'esser_mech', 
#               'theta_eq' : -54,'tau_theta' : 1,'tau_spike' : 0.48/7,'tau_m' : 7/7,'gNa_leak' : 0.2,
#               'gK_leak' : 1.0, 'tspike' : 0.75}  					# soma hh mechanisms
# cellRule['secs']['soma']['ions'] = {'na':{'e':30.0},'k':{'e':-90}}
# cellRule['secs']['soma']['vinit'] = -75.263
# netParams.cellParams['Inh_rule'] = cellRule


# Synaptic mechanism parameters
netParams.synMechParams['exc'] = {'mod': 'Exp2Syn_esser','gpeak':0.1, 'tau_m': 1,'tau1': 0.5,'tau2': 2.4, 'e': 0} #excitatory synaptic mechanism
# netParams.synMechParams['NMDA'] = {'mod': 'NMDA_esser','gpeak':1, 'tau_m': 13/13,'tau1': 4,'tau2': 40, 'e': 0} #excitatory synaptic mechanism

# stimulation
# netParams.stimSourceParams['bkg'] = {'type': 'NetStim','rate': 10, 'noise': 0.5}
# # stim connects to the cells
# netParams.stimTargetParams['bkg->L23Exc'] = {'source': 'bkg', 'conds': {'cellType': 'L23Exc'}, 'weight': 1, 'delay': 2, 'synMech': 'exc'}
# Cell connectivity rules
netParams.connParams['L23->L5'] = {
 	'preConds': {'pop': 'L23exc'}, 'postConds': {'pop': 'L5exc'},  #  S -> M
 	'probability': 1, 		# probability of connection
 	'weight': 2, 			# synaptic weight 
 	'delay': 0.5,					# transmission delay (ms) 
 	'sec': 'soma',				# section to connect to
 	'loc': 0.5,
 	'synMech': 'exc'}   		# target synapse 
#
l1 = [0,1,2,5]
l2 = [0,1,2,5]
l3 = [0,1,2,5]
# current injection dur 0.2ms amp 3000 (threshold 1450)
netParams.stimSourceParams['Input_1'] = {'type': 'IClamp', 'del': 0, 'dur': 0.2, 'amp': 3000}
netParams.stimTargetParams['Input_1->L23exc'] = {'source': 'Input_1', 'sec':'soma', 'loc': 0.5, 'conds': {'pop':'L23exc','cellList':l1}}

# netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': 1, 'noise': 0}
# netParams.stimTargetParams['bkg->PYR'] = {'source': 'bkg', 'conds': {'cellType': ['L5exc']}, 'weight': 1, 'delay': 100, 'synMech': 'NMDA'}

# netParams.stimSourceParams['Input_2'] = {'type': 'IClamp', 'del': 0, 'dur': 0.2, 'amp': 3000}
# netParams.stimTargetParams['Input_2->L5exc'] = {'source': 'Input_2', 'sec':'soma', 'loc': 0.5, 'conds': {'pop':'L5exc','cellList':l2}}

# netParams.stimSourceParams['Input_3'] = {'type': 'IClamp', 'del': 0, 'dur': 0.2, 'amp': 3000}
# netParams.stimTargetParams['Input_3->inh'] = {'source': 'Input_3', 'sec':'soma', 'loc': 0.5, 'conds': {'pop':'inh','cellList':l3}}


#Simulation options  
simConfig = specs.SimConfig()      # object of class SimConfig to store simulation config
simConfig.duration = 100          # Duration of the simulation, in ms
simConfig.dt = 0.001                       # Internal integration timestep to use
simConfig.verbose = False                   # Show detailed messages 
simConfig.recordTraces = {'V_soma': {'sec':'soma','loc':0.5, 'var' :'v'}} # Dict with traces to record
simConfig.recordStep = 0.01                  # Step size in ms
simConfig.recordStim = True
simConfig.saveTxt = True
simConfig.filename = 'model_output' # file output name
simConfig.savePickle = False           #Save params, network and sim output to pickle file

simConfig.analysis['plotRaster'] = False
simConfig.analysis['plotTraces'] = {'include':[('L23exc',0),('L5exc',0),('inh',0)],'overlay':False,'oneFigPer':'trace'}
simConfig.analysis['plot2Dnet'] = False

# sim.initialize(                       # create network object and set cfg and net params
#     simConfig = simConfig,   # pass simulation config and network params as arguments
#     netParams = netParams)
# sim.net.createPops()                      # instantiate network populations
# sim.net.createCells()                     # instantiate network cells based on defined populations
# sim.net.connectCells()                    # create connections between cells based on params
# sim.setupRecording()                  # setup variables to record for each cell (spikes, V traces, etc)
sim.create(netParams, simConfig)

# Use Netcon.event to do synaptic activation 
# the first cell in L5
sim.net.cells[10].conns[5]['hObj'].event(50)
sim.net.cells[10].conns[6]['hObj'].event(50)
sim.net.cells[10].conns[7]['hObj'].event(50)
sim.net.cells[10].conns[8]['hObj'].event(50)
sim.net.cells[10].conns[9]['hObj'].event(50)
sim.net.cells[10].conns[4]['hObj'].event(50)
sim.net.cells[10].conns[3]['hObj'].event(50)
sim.net.cells[10].conns[2]['hObj'].event(50)
sim.net.cells[10].conns[1]['hObj'].event(50)
sim.net.cells[10].conns[0]['hObj'].event(50)


# conns = [[0,0],[3,1],[4,2]]
# netParams.popParams['vecstim_0'] = {'cellModel': 'VecStim', 'numCells': 10, 'spkTimes':[70]}
# netParams.connParams['vecstim_0->myPop'] = {
#     'preConds': {'pop': 'vecstim_0'}, 
#     'postConds': {'pop': 'L5exc'},
#     # 'synMech': 'exc',
#     # 'weight': 5,                    
#     # 'delay': 0.5,
#     'connList': conns}
# sim.create(netParams, simConfig)

# %% setup recording and run simulation
sim.runSim()                          # run parallel Neuron simulation
sim.gatherData()                      # gather spiking data and cell info from each node
sim.saveData()                        # save params, cell info and sim output to file (pickle,mat,txt,etc)
sim.analysis.plotData()                   # plot spike raster

# # Create network and run simulation
# sim.createSimulateAnalyze(netParams = netParams, simConfig = simConfig)