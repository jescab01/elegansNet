

setwd("~/elegansProject/elegansPharynx/R analysis/Parameters")
library("dplyr", lib.loc="~/anaconda3/envs/rstudio/lib/R/library")
library("ggplot2", lib.loc="~/anaconda3/envs/rstudio/lib/R/library")



paramTest=read.csv('dataG_Thu Jun 20 18:36:41 2019(weights).csv')
# paramTestB=read.csv('data_Mon Apr  8 19:41:57 2019.csv')
# paramTestC=read.csv('data_Tue Apr  9 10:38:00 2019.csv')
# paramTest=rbind(paramTestA,paramTestB,paramTestC)
# rm(paramTestA, paramTestB, paramTestC)


paramTest1=mutate(paramTest, surviveBinary = surviveTime, rrp2spike=inATT-rrp2rest, ocrrp2spike=rrp2spike/(rrp2spike+rrp2rest))

paramTest1$surviveBinary[paramTest1$surviveBinary!=50]=0
paramTest1$surviveBinary[paramTest1$surviveBinary==50]=1


##### working on survival

modelsurv=glm(surviveBinary~RI+c+att, data = paramTest1, family = "binomial")
summary(modelsurv)

ggplot(paramTest1, aes(c, surviveBinary, group=as.factor(RI), colour=as.factor(RI))) +
  geom_smooth(method = 'glm', method.args = list(family=binomial))+
  xlab("Synaptic efficacy (c)")+
  ylab("Persistance probability")+
  labs(colour = "Initial\nactivity\n(RI)")


#### Working on minimum activity node
filtered=filter(paramTest1, c==0.5, RI==0.4| RI==0.3|RI==0.5)
sampled=sample_n(paramTest1, 1000)
ggplot(sampled, aes(c, minNodeActivity, group=as.factor(RI), colour=as.factor(RI))) +
  geom_jitter()+
  xlab("Synaptic efficacy (c)")+
  ylab("minNodeActivity")+
  labs(colour = "Initial\nactivity\n(RI)")


##### working on attenuation coefficient

filtered=filter(paramTest1, surviveBinary==1)

modelrrp=glm(ocrrp2spike~att+c+RI+Psens, data = filtered, family = "binomial")
summary(modelrrp)


filtered2plot=filter(paramTest1, surviveBinary==1, c==0.16|c==0.18|c==0.14|c==0.1|c==0.2|c==0.25)
sampled=sample_n(filtered2plot, 15000)

ggplot(sampled, aes(att, ocrrp2spike, group=c, colour=as.factor(c))) +
  geom_jitter(size=0.5)+
  geom_smooth(method = 'glm', method.args = list(family=binomial), se=F)+
  xlab("attenuation coefficient (att)")+
  ylab("Attenuated spikes \n(normalized)")+
  labs(colour="Synaptic\neffcicacy")

ggplot(sampled, aes(RI, ocrrp2spike))+
  geom_jitter()+
  geom_smooth()
  


  #Distributions of rrp2rest and rrp2spike
datasurvive=filter(paramTest1, surviveBinary==1)
ggplot(datasurvive, aes(rrp2rest))+
  geom_histogram(binwidth = 3, colour="red")+
  geom_histogram(aes(rrp2spike), binwidth = 5, colour="grey")

mutation=mutate(paramTest1, normalizedrrp2spike=rrp2spike/max(rrp2spike))
mutation=filter(mutation, RI==0.05 & c==0.2 | c==0.275 |c==0.3| c==0.35 |c==0.5)
sampled2=sample_n(mutation, 3000)

ggplot(sampled2, aes(att, normalizedrrp2spike, group=c, colour=as.factor(c)))+
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









