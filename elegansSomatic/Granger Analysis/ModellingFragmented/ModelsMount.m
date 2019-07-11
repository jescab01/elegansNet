% mount models after fragmented analysis
load data_somatic.mat
load SomaticModels2ht.mat
aicF=aic;
bhatF=bhat;
LLKf=LLK;


for i=2:2:20
    str=strcat('SomaticModels',num2str(i),'ht.mat');
    load (str)
    [ht,~]=size(aicF);
    [htn,~]=size(aic);

    aicF(ht+1:htn,:)=aic(ht+1:htn,:);
    bhatF(ht+1:htn,:)=bhat(ht+1:htn,:);
    LLKf(ht+1:htn,:)=LLK(ht+1:htn,:);
end


aic=aicF;
bhat=bhatF;
LLK=LLKf;

save('ModelsF', 'aic', 'LLK', 'bhat', 'X')
clear aicF bhatF LLKf htn ht str i