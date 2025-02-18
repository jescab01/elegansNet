% Load data
load data_pharynx.mat;

% Choose automatically ht with minimum aic.
aicM=aic;
aicM(aic==0)=NaN;
[V,I]=min(aicM);

ht = I;

% Dimension of data (L: length, N: number of neurons)
[L,N] = size(X);

% Re-optimizing a model after excluding a trigger neuron's effect and then
% Estimating causality matrices based on the likelihood ratio
for target = 1:N
    LLK0(target) = LLK(ht(target),target);              % Likelihood of full model
    % LLK0(target) = log_likelihood_win(bhat{ht(target),target},X,ht(target),target);
    for trigger = 1:N
        % MLE after excluding trigger neuron
        [bhatc{target,trigger}] = glmcausal(X,target,trigger,ht(target),200,2);
        
        % Log likelihood obtained using a new GLM parameter and data, which exclude trigger
        LLKC(target,trigger) = log_likelihood_causal(bhatc{target,trigger},X,trigger,ht(target),target,2);
        
        % Log likelihood ratio
        LLKR(target,trigger) = LLKC(target,trigger) - LLK0(target);
        
        % Sign (excitation and inhibition) of interaction from trigger to target
        % Averaged influence of the spiking history of trigger on target
        SGN(target,trigger) = sign(sum(bhat{ht(target),target}(ht(target)/2*(trigger-1)+2:ht(target)/2*trigger+1)));
        disp ('Calculating causal models')
        disp ('Target neuron: ')
        disp (target)
        disp ('Trigger neuron: ')
        disp (trigger)
    end
end

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
save ('PharynxGC1PROBE','bhatc','LLK0','LLKC','LLKR','D','SGN','Phi','Psi1','Psi2','ht')