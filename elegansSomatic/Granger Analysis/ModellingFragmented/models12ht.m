%clear all;

%%% Load data from simulations
%  X=table2array(X);
%  X=logical(X);


% load data_sim_9neuron.mat;     % 9-neuron network
% load data_sim_hidden.mat;      % 5-neuron network with hidden feedback
 load data_somatic.mat

% Dimension of input data (L: length, N: number of neurons)
[L,N] = size(X);

% To fit GLM models with different history orders
for neuron = 1:N                            % neuron
    for ht = 12                         % history, when W=2ms
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
    for ht = 12
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
% a=round(sqrt(N)+0.5);
%  
% figure(neuron);
% for neuron = 1:N
%     subplot(a,a,neuron)
%     plot(aic(2:2:20,neuron));
% end


% Save results
%save('result_sim','bhat','aic','LLK');
save('SomaticModels12ht','bhat','aic','LLK')

% Identify Granger causality
%CausalTest;