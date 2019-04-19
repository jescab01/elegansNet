

setwd("~/elegansProject/elegansNet/data/parameterTesting")
library("dplyr", lib.loc="~/anaconda3/envs/rstudio/lib/R/library")
library("ggplot2", lib.loc="~/anaconda3/envs/rstudio/lib/R/library")



paramTest=read.csv('dataN_Tue Apr 16 12:00:30 2019.csv')
# paramTestB=read.csv('data_Mon Apr  8 19:41:57 2019.csv')
# paramTestC=read.csv('data_Tue Apr  9 10:38:00 2019.csv')
# paramTest=rbind(paramTestA,paramTestB,paramTestC)
# rm(paramTestA, paramTestB, paramTestC)


paramTest1=mutate(paramTest, surviveBinary = surviveTime, ocrrp2spike=rrp2spike/(rrp2spike+rrp2rest))

paramTest1$surviveBinary[paramTest1$surviveBinary!=50]=0
paramTest1$surviveBinary[paramTest1$surviveBinary==50]=1


##### working on survival

modelsurv=glm(paramTest1$surviveBinary~paramTest1$RI+paramTest1$c+paramTest1$hpV+paramTest1$Psens)
summary(modelsurv)

ggplot(paramTest1, aes(c, surviveBinary, group=as.factor(RI), colour=as.factor(RI))) +
  geom_smooth(method = 'glm', method.args = list(family=binomial))



##### working on RRP usage

filtered=filter(paramTest1, surviveBinary==1, c==0.2 | c==0.3 | c==0.4 | c==0.6)
#filtered$c=as.factor(filtered$c)
sampled=sample_n(filtered, 1000)

ggplot(sampled, aes(hpV, ocrrp2spike, group=c, colour=as.factor(c))) +
  geom_jitter()+
  geom_smooth(se=F)

ggplot(sampled, aes(RI, ocrrp2spike))+
  geom_jitter()+
  geom_smooth()
  
modelrrplinear=lm(paramTest1$ocrrp2spike~paramTest1$hpV+paramTest1$c+paramTest1$RI+paramTest1$Psens)
summary(modelrrplinear)




##################### 

## Working with randomSens model

psensmutation=mutate(filtered, ocactive= active/50, ocactiveG= activeG/(11*active), 
                     ocactiveSG= activeSG /(3*activeG), ocactiveNode= activeNode/(10*activeSG))



ggplot(psensmutation, aes(Psens, ocactive))+
  geom_point()+
  scale_y_continuous(limits = c(0,0.5))

ggplot(psensmutation, aes(Psens,activeG))+
  geom_point()

ggplot(psensmutation, aes(Psens,activeSG))+
  geom_point()

ggplot(psensmutation, aes(Psens,activeNode))+
  geom_point()









