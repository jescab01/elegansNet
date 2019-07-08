setwd("~/elegansProject/elegansPharynx/R analysis/Parameters")
library("dplyr", lib.loc="~/anaconda3/envs/rstudio/lib/R/library")
library("ggplot2", lib.loc="~/anaconda3/envs/rstudio/lib/R/library")



paramTest=read.csv('dataPharynx_Mon Jul  1 22:16:38 2019.csv')
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


#### Working on nodes minimum activity
modelMNA=glm(minNodeActivity~att+c+RI, data = paramTest1)
summary(modelMNA)

ggplot(paramTest1, aes(c, minNodeActivity, group=as.factor(RI), colour=as.factor(RI))) +
  geom_jitter(size=0.6)+
  geom_smooth()+
  xlab("Synaptic efficacy (c)")+
  ylab("minNodeActivity")+
  labs(colour = "Initial\nactivity\n(RI)")

ggplot(paramTest1, aes(c, minNodeActivity, group=as.factor(att), colour=as.factor(att))) +
  geom_jitter(size=0.6)+
  geom_smooth()+
  ylab("minNodeActivity")+
  labs()


##### working on attenuation coefficient
# filtered=filter(paramTest1, surviveBinary==1)

modelrrp=glm(ocrrp2spike~att+c+RI+Psens, data = paramTest1, family = binomial)
summary(modelrrp)

#filtered2plot=filter(paramTest1, surviveBinary==1, c==0.2|c==0.3|c==0.5|c==0.7|c==0.9)
sampled=sample_n(paramTest1, 15000)

ggplot(sampled, aes(att, ocrrp2spike, group=c, colour=as.factor(c))) +
  geom_jitter(size=0.5)+
  geom_smooth(method = 'glm', method.args = list(family=binomial), se=F)+
  xlab("attenuation coefficient (att)")+
  ylab("Attenuated spikes \n(normalized)")+
  labs(colour="Synaptic\neffcicacy")

ggplot(sampled, aes(c, ocrrp2spike, group=att, colour=as.factor(att))) +
  geom_jitter(size=0.5)+
  geom_smooth(method = 'glm', method.args = list(family=binomial), se=F)+
  xlab("Synaptic efficacy")+
  ylab("Attenuated spikes \n(normalized)")+
  labs(colour="Attenuation\ncoefficient")



  # Distributions of rrp2rest and rrp2spike
datasurvive=filter(paramTest1, surviveBinary==1)
ggplot(datasurvive, aes(rrp2rest))+
  geom_histogram(binwidth = 3, alpha=0.5)+
  geom_histogram(aes(rrp2spike), binwidth = 3, alpha=0.5)
  


##################### 
## Working with randomSens model

cycles=12
nG=1
nSG=3
avgN=(5+5+3)/3 #Average number of neurons per group.

psens=mutate(sampled, ocsens= sens/cycles, ocsensG=sensG/(nG*sens), 
                     ocsensSG=sensSG/(nSG*sensG), ocsensNode= sensNode/(avgN*sensSG))

# Proportions. Hopefully it is a stright line.
ggplot(psens, aes(Psens, ocsens))+
  geom_point(alpha=0.1, color='grey40')+ 
  stat_summary(fun.y = "mean", colour = "darkred", size = 4,shape=18, geom = "point")+
  ylab('Number of stimulations')

ggplot(psens, aes(Psens,ocsensG))+
  geom_point(alpha=0.1, color='grey40')+ 
  stat_summary(fun.y = "mean", colour = "darkred", size = 4,shape=18, geom = "point")+
  ylab('Number of activated groups')

ggplot(psens, aes(Psens,ocsensSG))+
  geom_point(alpha=0.1, color='grey40')+ 
  stat_summary(fun.y = "mean", colour = "darkred", size = 4,shape=18, geom = "point")+
  ylab('Number of activated subgroups')

ggplot(psens, aes(Psens,ocsensNode))+
  geom_point(alpha=0.1, color='grey40')+ 
  stat_summary(fun.y = "mean", colour = "darkred", size = 4,shape=18, geom = "point")+
  ylab('Number of activated nodes')


## Absolute numbers.
ggplot(psens, aes(Psens, sens))+
  geom_point(alpha=0.1, color='grey40')+ 
  stat_summary(fun.y = "mean", colour = "darkred", size = 4,shape=18, geom = "point")+
  ylab('Number of stimulations')

ggplot(psens, aes(Psens,sensG))+
  geom_point(alpha=0.1, color='grey40')+ 
  stat_summary(fun.y = "mean", colour = "darkred", size = 4,shape=18, geom = "point")+
  ylab('Number of activated groups')

ggplot(psens, aes(Psens,sensSG))+
  geom_point(alpha=0.1, color='grey40')+ 
  stat_summary(fun.y = "mean", colour = "darkred", size = 4,shape=18, geom = "point")+
  ylab('Number of activated subgroups')

ggplot(psens, aes(Psens,sensNode))+
  geom_point(alpha=0.1, color='grey40')+ 
  stat_summary(fun.y = "mean", colour = "darkred", size = 4,shape=18, geom = "point")+
  ylab('Number of activated nodes')
  







