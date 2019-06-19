%clear all;

%  activity=table2array(ActivityTueJun181224422019);
%  activity=logical(activity);
%   X=activity;

% Load simulated data
% load data_sim_9neuron.mat;     % 9-neuron network
% load data_sim_hidden.mat;      % 5-neuron network with hidden feedback
load dataPharynx.mat

% Dimension of input data (L: length, N: number of neurons)
[L,N] = size(X);

% To fit GLM models with different history orders
for neuron = 1:N                            % neuron
    for ht = 2:2:10                         % history, when W=2ms
        [bhat{ht,neuron}] = glmwin(X,neuron,ht,200,2);
        disp ('Calculating Models')
        disp ('Neuron: ')
        disp (neuron)
        disp ('ht: ')
        disp (ht)
    end
end

% To select a model order, calculate AIC
for neuron = 1:N
    for ht = 2:2:10
        LLK(ht,neuron) = log_likelihood_win(bhat{ht,neuron},X,ht,neuron,2); % Log-likelihood
        aic(ht,neuron) = -2*LLK(ht,neuron) + 2*(N*ht/2 + 1);                % AIC
        disp ('Calculating AIC')
        disp ('Neuron: ')
        disp (neuron)
        disp ('ht: ')
        disp (ht)
    end
end

% % To plot AIC 
a=round(sqrt(N)+0.5)
 
figure(neuron);
for neuron = 1:N
    subplot(a,a,neuron)
    plot(aic(2:2:10,neuron));
end

% Save results
%save('result_sim','bhat','aic','LLK');
save('PharynxModels','bhat','aic','LLK')

% Identify Granger causality
% CausalTest;