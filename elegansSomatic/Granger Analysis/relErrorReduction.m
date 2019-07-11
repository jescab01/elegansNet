% trying to simplyfy aic model selection with an
% additional criterion for penalizing parameters

[L,N] = size(X);

for neuron=1:N
    for ht=2:2:20
        Ered(ht,neuron)=(aic(2,neuron)/aic(ht,neuron));
    end
end

for neuron=1:N
    for ht=4:2:20
        relEred(ht,neuron)=Ered(ht,neuron)-Ered(ht-2,neuron);
    end
end

[~,Ir]=max(relEred);

% To plot relEred
a=round(sqrt(N/3)+0.5);
 
figure(1);
for neuron = 1:N/3
    subplot(a,a,neuron)
    plot(relEred(2:2:14,neuron));
end

figure(2);
for neuron = N/3:2*N/3
    subplot(a,a,neuron)
    plot(relEred(2:2:14,neuron));
end

figure(3);
for neuron = 2*N/3:N
    subplot(a,a,neuron)
    plot(relEred(2:2:14,neuron));
end


