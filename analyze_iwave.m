%% function that generate scatter plot of L23,L5,Inh population in microcircuit model
% input: 1. numcell: number of cell in the cellType
%        2. numinput: number of poisson input for cellType
%        3. cellType: 1)L23, 2)L5, 3)Inh
%        4. inconn: if intracortical connection is on 1---on 0---off
%        5. binsize: bin width of the histogram curve (ms)
%        6. dur: duration of the simulation (ms)
function [meanfr,stdfr,hc,tvec] = analyze_iwave (numcell, cellType, numpulse, binsize,TMStarget,stimint,stimonset,tpre,tpost)
% load the data out from NetPyNe
% determine if intracortical connection is on
if numpulse == 1
    pulse = 'single';
elseif numpulse == 2
    pulse = 'paired';
end
data = load(sprintf('raster_%s_%s_%s_%s.mat',TMStarget,stimint,pulse,cellType));
% clr = get(gca, 'colororder');

%% Plot histogram
ind = []; inind = [];
spkt = []; inspkt = [];
for i = 1:length(data.data.spkInds)
    if data.data.spkInds(i)<numcell %ind of L23 is 0-99
        ind = [ind data.data.spkInds(i)];
        spkt = [spkt data.data.spkTimes(i)];
    else
        inind = [inind data.data.spkInds(i)];
        inspkt = [inspkt data.data.spkTimes(i)];
    end
end

% extract I waves interval (5ms before the stim onset and 10 ms after stim
% onset)
spkt2 = spkt(spkt>=(stimonset-tpre) & spkt<=(stimonset+tpost));
ind2 = ind(spkt>=(stimonset-tpre) & spkt<=(stimonset+tpost));
%calculate histcount 
dur = tpost+tpre;
edges = (stimonset-tpre):binsize:(stimonset+tpost); 
[hc, edge] = histcounts(spkt2,edges);
% w = gausswin(binsize);
% hc = filter(w,1,hc);
tvec = edge(2:end) - diff(edge)./2;

% calculate FR for each neuron within 10 ms after stim
ind3 = ind2(spkt2>stimonset+0.1);
fr = zeros(1,numcell);
for j = 0:max(numcell-1)
    frpercell = length(find(ind3 == j)); % number of spk / 10 milisecond
    fr(j+1) = frpercell;
end
fr = fr * 100;  %convert spk/10ms to spk/second 
meanfr = mean(fr); 
stdfr = std(fr);
% meanfrinL23 = mean(frL23(1:(num_L23+num_inL23)));
% stdfrinL23 = std(frL23(1:num_L23+num_inL23));


figure; 
% scatter(dataL23.data.spkTimes,dataL23.data.spkInds,'.'); 
scatter(spkt2,ind2,'.'); 
hold on
yyaxis right; 
plot(tvec,hc./binsize*1000/numcell,'r','LineWidth',1)
ylabel('population rate (sp/s)')
set(gca,'ycolor','r') 
% ylim ([0 15])
yyaxis left
ylabel(sprintf('ind %s',cellType))
hold off
xlabel('time (ms)')