

setwd("~/elegansProject/elegansNet/data/parameterTesting")
library("dplyr", lib.loc="~/anaconda3/envs/rstudio/lib/R/library")
library("ggplot2", lib.loc="~/anaconda3/envs/rstudio/lib/R/library")



paramTest=read.csv('data_Sun Apr  7 23:26:32 2019.csv')

paramTest1=mutate(paramTest, surviveBinary = surviveTime, ocrrp2spike=rrp2spike/(rrp2spike+rrp2rest))

paramTest1$surviveBinary[paramTest1$surviveBinary!=50]=0
paramTest1$surviveBinary[paramTest1$surviveBinary==50]=1



##### working on survival

modelsurv=glm(paramTest1$surviveBinary~paramTest1$RI+paramTest1$c+paramTest1$hpV)
summary(modelsurv)

ggplot(paramTest1, aes(c, surviveBinary, group=RI, colour=RI)) +
  geom_smooth(method = 'glm', method.args = list(family=binomial))



##### working on RRP usage

filtered=filter(paramTest1, surviveBinary==1)
filtered$c=as.factor(filtered$c)
sampled=sample_n(filtered, 1000)

ggplot(filtered, aes(hpV, ocrrp2spike, group=RI, colour=RI))+
  geom_smooth(se=F)
  
modelrrp=glm(paramTest1$ocrrp2spike~paramTest1$hpV+paramTest1$c+paramTest1$RI)
summary(modelrrp)


