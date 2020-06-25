--------------------------------------------------------------------------
                    nhp_tms_microcircuit NetPyNe implementation
--------------------------------------------------------------------------

--------------------------------------------------------------------------
                      Running instructions 
--------------------------------------------------------------------------

You will need the NEURON simulator in order to run this simulation.

Once you have NEURON installed you will need to compile the .mod files
included in the esser_mod_new folder. 


1. run run_esser_spon.py to simulate spontaneous activity of the model 
(run run_microcircuit_spon.slurm on cluster)
2. run run_esser_TMS.py to simulate model response to TMS
(run run_microcircuit_TMS2.slurm on cluster)
Simulations will save rasters as pickle file in dataset folder
If you run simulation on cluster, you need to transfer pickle file in the local dataset folder

3. readnsave.py read saved pickle files from dataset folder and save data as .mat file
4. plotraster.mat plot raster  



