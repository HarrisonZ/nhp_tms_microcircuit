%% Plot raster of spontaneuous activity
clear all
binsize = 10; dur = 1000;
cellType = 'Inh';
syntype = 2; % 1: separate AMPA&NMDA / GABAA&GABAB 2: combine syn
if syntype == 1
    addpath (pwd,'dataset')
elseif syntype == 2
    addpath (pwd,'data_combinesyn')
end
inconn = 1 ; % intracortical connection on
numcell = 50;  %num of cell type
numinput = 100; % num of Poisson inputs
[meanfr,stdfr,hc,tvec] = esser_scatter (numcell, numinput, cellType, inconn, binsize, dur);
%% Plot raster of response to TMS 
clear all
binsize = 10; dur = 1000;
cellType = 'L23';
TMStarget = 'TMSall';
stimint = 'stim50' ;
syntype = 2; % 1: separate AMPA&NMDA / GABAA&GABAB 2: combine syn
if syntype == 1
    addpath (pwd,'dataset')
elseif syntype == 2
    addpath (pwd,'data_combinesyn')
end
% TMStarget = 'test';
numpulse = 1 ; % intracortical connection on
numcell = 100;  %num of cell type
numinput = 100; % num of Poisson inputs
[meanfr1,stdfr1,hc1,tvec1] = esser_scatter_TMS (numcell, numinput, cellType, numpulse, binsize, dur,TMStarget,stimint);
%% Plot raster of I wave response 
clear all
binsize = 0.2;
cellType = 'Inh';
TMStarget = 'TMSall';
stimint = 'stim10' ;
stimonset = 200; %ms
tpre = 5;
tpost = 10;
syntype = 3; % 1: separate AMPA&NMDA / GABAA&GABAB 2: combine syn Iinj 3: combine syn old stim method
if syntype == 1
    addpath (pwd,'dataset')
elseif syntype == 2
    addpath (pwd,'data_combinesyn')
elseif syntype == 3
    addpath (pwd,'data_combinesyn_oldstim')
end
% TMStarget = 'test';
numpulse = 1 ; % intracortical connection on
numcell = 50;  %num of cell type
[meanfr2,stdfr2,hc2,tvec2] = analyze_iwave (numcell, cellType, numpulse, binsize,TMStarget,stimint,stimonset,tpre,tpost);
