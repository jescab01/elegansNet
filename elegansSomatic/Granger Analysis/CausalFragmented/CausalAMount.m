% mount models after fragmented analysis

load GC1A.mat
SGNF=SGN;
bhatcF=bhatc;
LLKCf=LLKC;
LLKRf=LLKR;

%checar que tengo que hacer

load SomaticModels4ht.mat
[ht,~]=size(aicF);
[htn,~]=size(aic);

aicF(ht+1:htn,:)=aic(ht+1:htn,:);
bhatF(ht+1:htn,:)=bhat(ht+1:htn,:);
LLKf(ht+1:htn,:)=LLK(ht+1:htn,:);


load SomaticModels6ht.mat
[ht,~]=size(aicF);
[htn,~]=size(aic);

aicF(ht+1:htn,:)=aic(ht+1:htn,:);
bhatF(ht+1:htn,:)=bhat(ht+1:htn,:);
LLKf(ht+1:htn,:)=LLK(ht+1:htn,:);

...

aic=aicF;
bhat=bhatF;
LLK=LLKf;

save('ModelsF', 'aic', 'LLK', 'bhat')
clear aic bhat LLK htn ht