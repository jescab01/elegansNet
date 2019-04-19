
library("dplyr", lib.loc="~/anaconda3/envs/rstudio/lib/R/library")
library("ggplot2", lib.loc="~/anaconda3/envs/rstudio/lib/R/library")
ct=read.csv('data/parameterTesting/Cw.csv')
et=read.csv('data/parameterTesting/Ew.csv')

ct=mutate(ct, cw= log(ct[,1]+1))


ggplot(ct, aes(cw))+
  geom_bar()

ggplot(ew, aes(X0))+
  geom_bar()

ln(10)
