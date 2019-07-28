%clear all;

% Load data
load ModelsF.mat
load ht.mat

% Dimension of data (L: length, N: number of neurons)
[L,N] = size(X);

% Preallocate to speed up the process
bhatc=cell(N,N);
LLKC=zeros(N,N);
LLKR=zeros(N,N);
SGN=zeros(N,N);

% Re-optimizing a model after excluding a trigger neuron's effect and then
% Estimating causality matrices based on the likelihood ratio
for target = 133
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


% Save results
save ('SomaticGC27c','bhatc','LLKC','LLKR','SGN')
