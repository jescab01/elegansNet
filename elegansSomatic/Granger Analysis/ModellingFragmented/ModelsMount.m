% mount models after fragmented analysis

load SomaticModels2ht.mat
aicF=aic;
bhatF=bhat;
LLKf=LLK;

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

load SomaticModels8ht.mat
[ht,~]=size(aicF);
[htn,~]=size(aic);

aicF(ht+1:htn,:)=aic(ht+1:htn,:);
bhatF(ht+1:htn,:)=bhat(ht+1:htn,:);
LLKf(ht+1:htn,:)=LLK(ht+1:htn,:);

load SomaticModels10ht.mat
[ht,~]=size(aicF);
[htn,~]=size(aic);

aicF(ht+1:htn,:)=aic(ht+1:htn,:);
bhatF(ht+1:htn,:)=bhat(ht+1:htn,:);
LLKf(ht+1:htn,:)=LLK(ht+1:htn,:);

load SomaticModels12ht.mat
[ht,~]=size(aicF);
[htn,~]=size(aic);

aicF(ht+1:htn,:)=aic(ht+1:htn,:);
bhatF(ht+1:htn,:)=bhat(ht+1:htn,:);
LLKf(ht+1:htn,:)=LLK(ht+1:htn,:);

load SomaticModels14ht.mat
[ht,~]=size(aicF);
[htn,~]=size(aic);

aicF(ht+1:htn,:)=aic(ht+1:htn,:);
bhatF(ht+1:htn,:)=bhat(ht+1:htn,:);
LLKf(ht+1:htn,:)=LLK(ht+1:htn,:);

load SomaticModels16ht.mat
[ht,~]=size(aicF);
[htn,~]=size(aic);

aicF(ht+1:htn,:)=aic(ht+1:htn,:);
bhatF(ht+1:htn,:)=bhat(ht+1:htn,:);
LLKf(ht+1:htn,:)=LLK(ht+1:htn,:);

load SomaticModels18ht.mat
[ht,~]=size(aicF);
[htn,~]=size(aic);

aicF(ht+1:htn,:)=aic(ht+1:htn,:);
bhatF(ht+1:htn,:)=bhat(ht+1:htn,:);
LLKf(ht+1:htn,:)=LLK(ht+1:htn,:);

load SomaticModels20ht.mat
[ht,~]=size(aicF);
[htn,~]=size(aic);

aicF(ht+1:htn,:)=aic(ht+1:htn,:);
bhatF(ht+1:htn,:)=bhat(ht+1:htn,:);
LLKf(ht+1:htn,:)=LLK(ht+1:htn,:);

aic=aicF;
bhat=bhatF;
LLK=LLKf;

save('ModelsF', 'aic', 'LLK', 'bhat')
clear aic bhat LLK htn ht