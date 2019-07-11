

setwd("~/elegansProject/elegansSomatic/R analysis/Parameters")
library("dplyr", lib.loc="~/anaconda3/envs/rstudio/lib/R/library")
library("ggplot2", lib.loc="~/anaconda3/envs/rstudio/lib/R/library")



paramTest=read.csv('dataSomatic_Sat Jul  6 09:19:37 2019.csv')
# paramTestB=read.csv('data_Mon Apr  8 19:41:57 2019.csv')
# paramTestC=read.csv('data_Tue Apr  9 10:38:00 2019.csv')
# paramTest=rbind(paramTestA,paramTestB,paramTestC)
# rm(paramTestA, paramTestB, paramTestC)


paramTest1=mutate(paramTest, surviveBinary = surviveTime, rrp2spike=inATT-rrp2rest, ocrrp2spike=rrp2spike/(rrp2spike+rrp2rest))

paramTest1$surviveBinary[paramTest1$surviveBinary!=50]=0
paramTest1$surviveBinary[paramTest1$surviveBinary==50]=1

################################### Sampling
sampled=sample_n(paramTest1, 40000)


##### working on survival -----

modelsurv=glm(surviveBinary~RI+c+att+Psens, data = paramTest1, family = "binomial")
summary(modelsurv)

ggplot(paramTest1, aes(c, surviveBinary, group=as.factor(RI), colour=as.factor(RI))) +
  geom_smooth(method = 'glm', method.args = list(family=binomial))+
  xlab("Synaptic efficacy (c)")+
  ylab("Persistance probability")+
  labs(colour = "Initial\nactivity\n(RI)")



#### Working on minimum activity node -----
# filtered=filter(paramTest1, c==0.5, RI==0.4| RI==0.3|RI==0.5)
ggplot(sampled, aes(c, minNodeActivity, group=as.factor(RI), colour=as.factor(RI))) +
  geom_jitter(size=0.7)+
  xlab("Synaptic efficacy (c)")+
  ylab("minNodeActivity")+
  labs(colour = "Initial\nactivity\n(RI)")


##### working on attenuation coefficient ------
modeladt=glm(ocrrp2spike~att+c+RI+Psens, data = paramTest1, family = "binomial")
summary(modeladt)

filtered=filter(paramTest1, c==0.1|c==0.15|c==0.2|c==0.25|c==0.3|c==0.35|c==0.41|c==0.45|c==0.5, surviveBinary==1)
ggplot(filtered, aes(att, ocrrp2spike, group=c, colour=as.factor(c))) +
  geom_jitter(size=0.5, alpha=0.1)+
  geom_smooth(method = 'glm', method.args = list(family=binomial), se=F)+
  xlab("attenuation coefficient (att)")+
  ylab("Attenuated spikes \n(normalized)")+
  labs(colour="Synaptic\neffcicacy")



  #Distributions of rrp2rest and rrp2spike
datasurvive=filter(paramTest1, surviveBinary==1)
ggplot(datasurvive, aes(rrp2rest))+
  geom_histogram(binwidth = 3, alpha=0.5)+
  geom_histogram(alpha=0.5, aes(rrp2spike), binwidth = 5)


#### Working with randomSens model -----

cycles=12
nG=1
nSG=3
avgN=(5+5+3)/3 #Average number of neurons per group.

psens=mutate(sampled, ocsens= sens/cycles, ocsensG=sensG/(nG*sens), 
             ocsensSG=sensSG/(nSG*sensG), ocsensNode= sensNode/(avgN*sensSG))

# Proportions. Hopefully stright lines.
ggplot(psens, aes(Psens, ocsens))+
  geom_point(alpha=0.1, color='grey40')+ 
  stat_summary(fun.y = "mean", colour = "darkred", size = 4,shape=18, geom = "point")+
  ylab('Proportion of stimulations')

ggplot(psens, aes(Psens,ocsensG))+
  geom_point(alpha=0.1, color='grey40')+ 
  stat_summary(fun.y = "mean", colour = "darkred", size = 4,shape=18, geom = "point")+
  ylab('Proportion of activated groups')

ggplot(psens, aes(Psens,ocsensSG))+
  geom_point(alpha=0.1, color='grey40')+ 
  stat_summary(fun.y = "mean", colour = "darkred", size = 4,shape=18, geom = "point")+
  ylab('Proportion of activated subgroups')

ggplot(psens, aes(Psens,ocsensNode))+
  geom_point(alpha=0.1, color='grey40')+ 
  stat_summary(fun.y = "mean", colour = "darkred", size = 4,shape=18, geom = "point")+
  ylab('Proportion of activated nodes')


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







