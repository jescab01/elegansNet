

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

modelsurv=glm(surviveBinary~RI+c+hpV+Psens, data = paramTest1, family = "binomial")
summary(modelsurv)

ggplot(paramTest1, aes(c, surviveBinary, group=as.factor(RI), colour=as.factor(RI))) +
  geom_smooth(method = 'glm', method.args = list(family=binomial))+
  xlab("Synaptic efficacy (c)")+
  ylab("Persistance probability")+
  labs(colour = "Initial\nactivity\n(RI)")




##### working on RRP usage

filtered=filter(paramTest1, surviveBinary==1)

modelrrplinear=lm(ocrrp2spike~hpV+c+RI+Psens, data = filtered)
summary(modelrrplinear)

modelrrp=glm(ocrrp2spike~hpV+c+RI+Psens, data = filtered, family = "binomial")
summary(modelrrp)


filtered2plot=filter(paramTest1, surviveBinary==1, c==0.2 | c==0.25 |c==0.3| c==0.35 |c==0.45)
#filtered$c=as.factor(filtered$c)
sampled=sample_n(filtered2plot, 20000)

ggplot(sampled, aes(hpV, ocrrp2spike, group=c, colour=as.factor(c))) +
  geom_jitter(size=0.1)+
  geom_smooth(method = "glm", method.args=list(family="binomial"),  se=T)+
  xlab("Hyperporlarization Value (hpV)")+
  ylab("Spikes from hyperpolarization state \n(normalized)")+
  labs(colour="Synaptic\neffcicacy")

ggplot(sampled, aes(RI, ocrrp2spike))+
  geom_jitter()+
  geom_smooth()
  

filtered2plot=filter(paramTest1, surviveBinary==1, c==0.3 & RI==0.05)#| RI==0.1 |RI==0.15| RI==0.2 |RI==0.25)
#filtered$c=as.factor(filtered$c)
sampled=sample_n(filtered2plot, 50000)

ggplot(filtered2plot, aes(hpV, ocrrp2spike, group=RI, colour=as.factor(RI))) +
  geom_jitter(size=0.1)+
  geom_smooth(method = "glm", method.args=list(family="binomial"),  se=F)


datasurvive=filter(paramTest1, surviveBinary==1)
ggplot(datasurvive, aes(rrp2rest))+
  geom_histogram(binwidth = 3, colour="red")+
  geom_histogram(aes(rrp2spike), binwidth = 5, colour="grey")

mutation=mutate(paramTest1, normalizedrrp2spike=rrp2spike/max(rrp2spike))
mutation=filter(mutation, RI==0.05 & c==0.2 | c==0.275 |c==0.3| c==0.35 |c==0.5)
sampled=sample_n(mutation, 50000)

ggplot(sampled, aes(hpV, normalizedrrp2spike, group=c, colour=as.factor(c)))+
  geom_jitter(size=0.5)+
  geom_smooth()



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









