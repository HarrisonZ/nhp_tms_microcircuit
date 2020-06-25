%% function that generate scatter plot of L23,L5,Inh population in microcircuit model
% input: 1. numcell: number of cell in the cellType
%        2. numinput: number of poisson input for cellType
%        3. cellType: 1)L23, 2)L5, 3)Inh
%        4. inconn: if intracortical connection is on 1---on 0---off
%        5. binsize: bin width of the histogram curve (ms)
%        6. dur: duration of the simulation (ms)
function [meanfr,stdfr,hc,tvec] = esser_scatter (numcell, numinput, cellType, inconn, binsize, dur)
% load the data out from NetPyNe
% determine if intracortical connection is on
if inconn == 0
    conn = 'inoff';
else
    conn = 'inon';
end
data = load(sprintf('raster_spon_%s_%s.mat',conn,cellType));
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
%calculate histcount 
[hc, edge] = histcounts(spkt,dur/binsize);
tvec = edge(2:end) - diff(edge)./2;
[hcin,edgein] = histcounts(inspkt,dur/binsize);
tvec2 = edgein(2:end) - diff(edgein)./2;

% calculate FR for each neuron in the population
fr = zeros(1,max(data.data.spkInds)+1);
for j = 0:max(data.data.spkInds)
    frpercell = length(find(data.data.spkInds == j)); % number of spk / 1second
    fr(j+1) = frpercell;
end
meanfr = mean(fr(1:numcell));
stdfr = std(fr(1:numcell));
% meanfrinL23 = mean(frL23(1:(num_L23+num_inL23)));
% stdfrinL23 = std(frL23(1:num_L23+num_inL23));


figure; 
% scatter(dataL23.data.spkTimes,dataL23.data.spkInds,'.'); 
scatter(spkt,ind,'.'); 
hold on
scatter(inspkt,inind,'.'); 
yyaxis right; 
plot(tvec,hc./binsize*dur/numcell,'r','LineWidth',1)
plot(tvec2,hcin./binsize*dur/numinput,'-','Color',[0.7500 0.7500 0],'LineWidth',1)
ylabel('population rate (sp/s)')
set(gca,'ycolor','r') 
% ylim ([0 15])
yyaxis left
ylabel(sprintf('ind %s',cellType))
hold off
xlabel('time (ms)')