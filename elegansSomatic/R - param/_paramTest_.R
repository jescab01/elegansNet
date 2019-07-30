setwd("~/elegansProject/elegansSomatic/R - param/")
library("dplyr")
library("ggplot2")

paramTest=read.csv('dataSomatic_Sat Jul  6 09:19:37 2019.csv')

paramTest1=mutate(paramTest, surviveBinary = surviveTime, rrp2spike=inATT-rrp2rest, ocrrp2spike=rrp2spike/(rrp2spike+rrp2rest))
paramTest1$surviveBinary[paramTest1$surviveBinary!=50]=0
paramTest1$surviveBinary[paramTest1$surviveBinary==50]=1


##### working on survival -----
modelsurv=glm(surviveBinary~RI+c+att+Psens, data = paramTest1, family = "binomial")
summary(modelsurv)

ggplot(paramTest1, aes(c, surviveBinary, group=as.factor(Psens), colour=as.factor(Psens))) +
  geom_smooth(method = 'glm', method.args = list(family=binomial))+
  xlab("Synaptic efficacy (c)")+
  ylab("Persistance probability")+
  xlim(0,0.35)+
  labs(colour = "Probability\nsensory\nstimulation\n(Psens)")+
  guides(color = guide_legend(reverse = TRUE))+
  ggtitle('Network persistence - Somatic')+
  theme(legend.title.align = 0.5)


#### Filter for survivals ----
# To control time length of simulations we focus on suvivals. 
survivals=filter(paramTest1, surviveBinary==1)


#### Working on minimum activity node -----
modelMNA=glm(minNodeActivity~RI+c+att+Psens, data = survivals, family = "poisson")
summary(modelMNA)

ggplot(survivals, aes(c, minNodeActivity, group=as.factor(att), colour=as.factor(att))) +
  geom_jitter(size=0.3)+
  geom_smooth(method = "glm",  method.args = list(family = "poisson"))+
  xlab("Synaptic efficacy (c)")+
  ylab("Potentials count")+
  xlim(0.2,0.7)+
  labs(colour = "Attenuation\ncoefficient\n(att)")+
  guides(color = guide_legend(reverse = TRUE))+
  ggtitle('Minimum Node Activity - Somatic')+
  theme(legend.title.align = 0.5)


##### working on attenuation coefficient. ----
# Binomial model for proportions
attc=cbind(survivals$rrp2spike, survivals$rrp2rest)
modelrrp=glm(attc~RI+c+att+Psens, data = survivals, family = 'binomial')
summary(modelrrp)

f2plot=filter(survivals, c==0.1|c==0.2|c==0.3|c==0.5|c==0.7)

ggplot(f2plot, aes(att, ocrrp2spike, group=c, colour=as.factor(c))) +
  geom_jitter(size=0.3, alpha=0.5)+
  geom_smooth(method = 'glm', method.args = list(family=binomial), se=F)+
  xlab("Attenuation coefficient (att)")+
  ylab("Proportion of attenuated potentials")+
  guides(color = guide_legend(reverse = TRUE))+
  labs(colour="Synaptic\neffcicacy\n(c)")+
  ggtitle('Attenuated Potentials - Somatic')+
  theme(legend.title.align = 0.5)


##### Working with Sensory stimulation ----
# Absolute numbers.
ggplot(survivals, aes(Psens, sens, group=Psens))+
  geom_boxplot(size = 0.3, outlier.size = 0.3, outlier.alpha = 0.5)+ 
  ylab('Number of stimulations')+
  theme_light()+
  ggtitle('Sensory Stimulation (Initialization) - Somatic')

ggplot(survivals, aes(Psens,sensG, group=Psens))+
  geom_boxplot(size = 0.3, outlier.size = 0.3, outlier.alpha = 0.5)+ 
  ylab('Number of activated groups')+
  theme_light()+
  ggtitle('Sensory Stimulation (Groups) - Somatic')

ggplot(survivals, aes(Psens,sensSG, group=Psens))+
  geom_boxplot(size = 0.3, outlier.size = 0.3, outlier.alpha = 0.5)+ 
  ylab('Number of activated subgroups')+
  theme_light()+
  ggtitle('Sensory Stimulation (Subgroups) - Somatic')

ggplot(survivals, aes(Psens,sensNode, group=Psens))+
  geom_boxplot(size = 0.3, outlier.size = 0.3, outlier.alpha = 0.5)+ 
  ylab('Number of activated nodes')+
  theme_light()+
  ggtitle('Sensory Stimulation (Cells) - Somatic')


#### Proportions. Hopefully it is a stright line. ----
# Check. Should show an averages at the level of the values implemented in envInput.py

### update cycles, nG, nSG and avgN with envInput.py in simulator. 

# cycles=12
# nG=1
# nSG=3
# avgN=(5+5+3)/3 #Average number of neurons per group.
# 
# psens=mutate(survivals, ocsens= sens/cycles, ocsensG=sensG/(nG*sens), 
#              ocsensSG=sensSG/(nSG*sensG), ocsensNode= sensNode/(avgN*sensSG))
# 
# ggplot(psens, aes(Psens, ocsens))+
#   geom_point(alpha=0.1, color='grey40')+ 
#   stat_summary(fun.y = "mean", colour = "darkred", size = 4,shape=18, geom = "point")+
#   ylab('Proportion of stimulations')
# 
# ggplot(psens, aes(Psens,ocsensG))+
#   geom_point(alpha=0.1, color='grey40')+ 
#   stat_summary(fun.y = "mean", colour = "darkred", size = 4,shape=18, geom = "point")+
#   ylab('Proportion of activated groups')
# 
# ggplot(psens, aes(Psens,ocsensSG))+
#   geom_point(alpha=0.1, color='grey40')+ 
#   stat_summary(fun.y = "mean", colour = "darkred", size = 4,shape=18, geom = "point")+
#   ylab('Proportion of activated subgroups')
# 
# ggplot(psens, aes(Psens,ocsensNode))+
#   geom_point(alpha=0.1, color='grey40')+ 
#   stat_summary(fun.y = "mean", colour = "darkred", size = 4,shape=18, geom = "point")+
#   ylab('Proportion of activated nodes')