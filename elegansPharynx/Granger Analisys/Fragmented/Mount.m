% mount models after fragmented analysis

load ht248.mat
aicF=aic;
bhatF=bhat;
LLKf=LLK;

load ht1014.mat
[ht,~]=size(aicF);
[htn,~]=size(aic);

aicF(ht+1:htn,:)=aic(ht+1:htn,:);
bhatF(ht+1:htn,:)=bhat(ht+1:htn,:);
LLKf(ht+1:htn,:)=LLK(ht+1:htn,:);


load xxxxx.mat
[ht,~]=size(aicF);
[htn,N]=size(aic);

aicF(ht+1:htn,:)=aic(ht+1:htn,:);
bhatF(ht+1:htn,:)=bhat(ht+1:htn,:);
LLKf(ht+1:htn,:)=LLK(ht+1:htn,:);