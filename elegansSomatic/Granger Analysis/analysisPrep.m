% Preparing connectivity analysis data to export to R and analize there.

% load ModelsF.mat
% load GAf.mat
% load names

% Dimension of input data (L: length, N: number of neurons)
[L,N] = size(X);

% Create a cell array to add Phi and Psi connections
fConn={'from', 'to', 'connPhi', 'connPsi1', 'connPsi2', 'connWeight', 'connWxGC'};


% Add Model Weights to the cell array
for trigger = 1:N
    for target=1:N
        fConn{(trigger-1)*N+target,1}=names{2,trigger};
        fConn{(trigger-1)*N+target,2}=names{2,target};
        fConn{(trigger-1)*N+target,3}=Phi(target,trigger);
        fConn{(trigger-1)*N+target,4}=Psi1(target,trigger);
        fConn{(trigger-1)*N+target,5}=Psi2(target,trigger);
        fConn{(trigger-1)*N+target,6}=sum(bhat{ht(target),target}(ht(target)/2*(trigger-1)+2:ht(target)/2*trigger+1));
        fConn{(trigger-1)*N+target,7}=abs(Psi2(target,trigger))*sum(bhat{ht(target),target}(ht(target)/2*(trigger-1)+2:ht(target)/2*trigger+1));
    end
end


colnames = {'from', 'to', 'connPhi', 'connPsi1', 'connPsi2', 'connWeight', 'connWxGC'};
fConn=cell2table(fConn,'VariableNames',colnames);

writetable(fConn,'Results/fConn1Jul.csv')


%% provisional just functional weights

load ModelsF.mat
load names
fConn={'from', 'to', 'connWeight'};
% Dimension of input data (L: length, N: number of neurons)
[L,N] = size(X);

aicM=aic;
aicM(aic==0)=NaN;
[~,I]=min(aicM);

ht = I;

for trigger = 1:N
    for target=1:N
        fConn{(trigger-1)*N+target,1}=names{2,trigger};
        fConn{(trigger-1)*N+target,2}=names{2,target};
        fConn{(trigger-1)*N+target,3}=sum(bhat{ht(target),target}(ht(target)/2*(trigger-1)+2:ht(target)/2*trigger+1));
    end
end


colnames = {'from', 'to', 'connWeight'};
fConn=cell2table(fConn,'VariableNames',colnames);

writetable(fConn,'Results/fConnWonly1Jul.csv')