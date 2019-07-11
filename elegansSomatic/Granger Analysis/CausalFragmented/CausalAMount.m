% mount models after fragmented analysis

load GC1A.mat
bhatcF=bhatc;
LLKCf=LLKC;
LLKRf=LLKR;
SGNF=SGN;

for i=1:7
    str=strcat('GC',num2str(i),'A.mat');
    disp(str)
    load (str)
    [tg,~]=size(bhatcF);
    [tgn,~]=size(bhactc);

    bhatcF(tg+1:tgn,:)=bhatc(tg+1:tgn,:);
    LLKCf(tg+1:tgn,:)=LLKC(tg+1:tgn,:);
    LLKRf(tg+1:tgn,:)=LLKR(tg+1:tgn,:);
    SGNF(tg+1:tgn,:)=SGN(tg+1:tgn,:);
end


bhatc=bhatcF;
LLKC=LLKCf;
LLKR=LLKRf;
SGN=SGNF;

save('GAf', 'bhatc', 'LLKC', 'LLKR', 'SGN')
clear bhatcF LLKCf LLKRf SGNF i str