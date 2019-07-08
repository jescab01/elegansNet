%clear all;

% Load data
load ModelsF.mat

% Choose automatically hts with minimum aic.
aicM=aic;
aicM(aic==0)=NaN;
[V,I]=min(aicM);

ht = I;


% Dimension of data (L: length, N: number of neurons)
[L,N] = size(X);

% Re-optimizing a model after excluding a trigger neuron's effect and then
% Estimating causality matrices based on the likelihood ratio
for target = 121:160
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
% save('CausalMaps','bhatc','LLK0','LLKC','LLKR','D','SGN','Phi','Psi1','Psi2');
save ('GC4A','bhatc','LLK0','LLKC','LLKR','ht')
% save ('elegansMaps','bhatc','LLK0','LLKC','LLKR','D','SGN','Phi','Psi1','Psi2')