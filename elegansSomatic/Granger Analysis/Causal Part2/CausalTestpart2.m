%clear all;

% Load data
load SomaticGCpart1
load ht

N=length(ht);

% Granger causality matrix, Phi
Phi = -SGN.*LLKR;

% ==== Significance Test ====
% Causal connectivity matrix, Psi, w/o FDR
D = -2*LLKR;                                     % Deviance difference
alpha = 0.05;
for ichannel = 1:N
    temp1(ichannel,:) = D(ichannel,:) > chi2inv(1-alpha,ht(ichannel)/2);
    disp ('Calculating significance')
    disp ('Neuron: ')
    disp (ichannel)
end
Psi1 = SGN.*temp1;

% Causal connectivity matrix, Psi, w/ FDR
fdrv = 0.05;
temp2 = FDR(D,fdrv,ht);
Psi2 = SGN.*temp2;

% Plot the results
 figure(1);imagesc(Phi);xlabel('Triggers');ylabel('Targets');
 figure(2);imagesc(Psi1);xlabel('Triggers');ylabel('Targets');
 figure(3);imagesc(Psi2);xlabel('Triggers');ylabel('Targets');

% Save results
save ('SomaticGC','bhatc','LLKC','LLKR','D','SGN','Phi','Psi1','Psi2','ht')
