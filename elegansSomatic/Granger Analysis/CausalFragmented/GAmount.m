%%% Mount Granger Analysis results after fragmented analysis

% First mount multi-fragmented analysis (n: 20, 27, 38, 39, 42, 49)
% i.e. neurons for which we used one analysis per target neuron.
nodes=[20,27,38,39,42,49];
list={'e' 'd' 'c' 'b' 'a'};

for a=1:length(nodes)
    load SomaticGC20a.mat
    bhatcF=bhatc;
    LLKCf=LLKC;
    LLKRf=LLKR;
    SGNf=SGN;
    
    for b=1:length(list)
        str=strcat('SomaticGC',num2str(nodes(a)),list(1,b),'.mat');
        name=strcat('SomaticGC',num2str(nodes(a)));
        load (str{1,1})
        
        bhatcF(nodes(a)*5-b+1,:)=bhatc(nodes(a)*5-b+1,:);
        LLKCf(nodes(a)*5-b+1,:)=LLKC(nodes(a)*5-b+1,:);
        LLKRf(nodes(a)*5-b+1,:)=LLKR(nodes(a)*5-b+1,:);
        SGNf(nodes(a)*5-b+1,:)=SGN(nodes(a)*5-b+1,:);
    
    bhatc=bhatcF;
    LLKC=LLKCf;
    LLKR=LLKRf;
    SGN=SGNf;
    save (name, 'bhatc', 'LLKC', 'LLKR', 'SGN')

    end
end



% Once with all pieces with the same shape, mount them.
load SomaticGC1.mat
bhatcF=bhatc;
LLKCf=LLKC;
LLKRf=LLKR;
SGNf=SGN;

for a=1:55
    str=strcat('SomaticGC',num2str(a),'.mat');
    load (str)

    bhatcF(a*5-4:a*5,:)=bhatc(a*5-4:a*5,:);
    LLKCf(a*5-4:a*5,:)=LLKC(a*5-4:a*5,:);
    LLKRf(a*5-4:a*5,:)=LLKR(a*5-4:a*5,:);
    SGNf(a*5-4:a*5,:)=SGN(a*5-4:a*5,:);
end

% Add last one independently
load SomaticGC56
bhatcF(276:279,:)=bhatc(276:279,:);
LLKCf(276:279,:)=LLKC(276:279,:);
LLKRf(276:279,:)=LLKR(276:279,:);
SGNf(276:279,:)=SGN(276:279,:);


bhatc=bhatcF;
LLKC=LLKCf;
LLKR=LLKRf;
SGN=SGNf;

save ('SomaticGCpart1', 'bhatc', 'LLKC', 'LLKR', 'SGN')