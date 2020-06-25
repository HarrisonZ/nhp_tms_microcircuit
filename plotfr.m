int = [10 20 30 40 50];
frl23 = [2,3,6,5,10]; errl23 = [14.0705 17.1447 23.868 21.9043 30.1511];
frl5 = [2 1 2 2 6]; errl5 = [14.0705 10 14.0705 14.07 23.86];
frInh = [12 38 40 46 34]; errInh = [32.8261 49.0314 49.4872 54.2481 47.85];
figure;
errorbar(int,frl23,errl23)
xlim([0 60])
ylim([-50 50])
xlabel('stim intensity (%)')
ylabel('L2/3 average firing rate (spike/second)')
figure;
errorbar(int,frl5,errl5)
xlim([0 60])
ylim([-50 50])
xlabel('stim intensity (%)')
ylabel('L5 average firing rate (spike/second)')
figure;
errorbar(int,frInh,errInh)
xlim([0 60])
ylim([-50 110])
xlabel('stim intensity (%)')
ylabel('Inh average firing rate (spike/second)')
