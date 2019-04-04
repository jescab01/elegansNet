
## Processing data. Generate Binary and timestep dataframe.


dfRIc=list()
probRIc=list()

tests=list.files('RIcData', full.names = FALSE)

for (test in tests) {
  RIs=list.files(paste('RIcData/',test, sep = ''))
  dfRIc[[test]]=list()
  probRIc[[test]]=data.frame(matrix(nrow = 71))
  
  for (ri in RIs){
    df=read.csv(paste('RIcData/',test,'/',ri, sep=''), na.strings = 'None', check.names = FALSE)
    df[is.na(df)]=1
    df[df!=1]=0
    dfRIc[[test]][[ri]]=df
    
    probRIc[[test]][[ri]]=colMeans(df)
  }
  rownames(probRIc[[test]]) = colnames(df)
  probRIc[[test]][[1]]=NULL
}

ggplot(probRIc[["paramTest0"]], aes(x=rownames(probRIc[["paramTest0"]]),
                                    y=probRIc[["paramTest0"]][["RI0.05.csv"]])) + 
         geom_point(size=1.5, shape=1) + geom_smooth(method=loess, se=TRUE,
                                                     fullrange= TRUE) +
  theme(panel.grid.minor.x = element_line(colour = 'white', size = 0.5 ))
    

## plotting 

# probabilities for success of simulation [with dfRIc data frame]

RI=c(0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5)

# for (ri in RI){
#   for (i in 0:9){  ## How many completed tests do you have? check at dfTimes.
#     plot(colnames(dfRIc[["paramTest0"]][['RI0.05.csv']]),
#          probRIc[[paste('paramTest',i,sep = '')]][[paste('RI',ri,'.csv',sep='')]],
#          main = paste('RandomInit=',as.character(ri),sep = ''),sub=paste('paramTest',i,'/binary',sep = ''), xlab='c', ylab='probability',
#          type='p', col='blue',pch=20,lty=1)
#   }
# }


## Averaging Data -

meanDataBinary=data.frame()
# meanDataTimes=list()

for (ri in RI){
  average=((probRIc[['paramTest0']][[paste('RI',ri,'.csv',sep = '')]]+
       probRIc[['paramTest1']][[paste('RI',ri,'.csv',sep = '')]]+
       probRIc[['paramTest2']][[paste('RI',ri,'.csv',sep = '')]]+
       probRIc[['paramTest3']][[paste('RI',ri,'.csv',sep = '')]]+
       probRIc[['paramTest4']][[paste('RI',ri,'.csv',sep = '')]]+
       probRIc[['paramTest5']][[paste('RI',ri,'.csv',sep = '')]]+
       probRIc[['paramTest6']][[paste('RI',ri,'.csv',sep = '')]]+
       probRIc[['paramTest7']][[paste('RI',ri,'.csv',sep = '')]]+
       probRIc[['paramTest8']][[paste('RI',ri,'.csv',sep = '')]]+
       probRIc[['paramTest9']][[paste('RI',ri,'.csv',sep = '')]])/10)
  meanDataBinary[[paste('RI',ri,sep = '')]]=average
}
  
  # average=((probTimes[['paramTest0']][[paste('RI',ri,'.csv',sep = '')]]+
  #         probTimes[['paramTest1']][[paste('RI',ri,'.csv',sep = '')]]+
  #         probTimes[['paramTest2']][[paste('RI',ri,'.csv',sep = '')]]+
  #         probTimes[['paramTest3']][[paste('RI',ri,'.csv',sep = '')]]+
  #         probTimes[['paramTest4']][[paste('RI',ri,'.csv',sep = '')]]+
  #         probTimes[['paramTest5']][[paste('RI',ri,'.csv',sep = '')]]+
  #         probTimes[['paramTest6']][[paste('RI',ri,'.csv',sep = '')]]+
  #         probTimes[['paramTest7']][[paste('RI',ri,'.csv',sep = '')]]+
  #         probTimes[['paramTest8']][[paste('RI',ri,'.csv',sep = '')]]+
  #         probTimes[['paramTest9']][[paste('RI',ri,'.csv',sep = '')]])/10)
  # meanDataTimes[[paste('RI',ri,sep = '')]]=average
#}


## Plotting average

par(mfrow=c(1,1))

plot(colnames(dfRIc[["paramTest0"]][['RI0.05.csv']]),
     meanDataBinary[['RI0.05']],
     main = paste('RandomInit=',as.character(ri),sep = ''),sub='Averaged data Binary', xlab='c', ylab='probability',
     type='p', col='blue',pch=20,lty=1)
par(new=T)

for (ri in RI[2:length(RI)]){
  plot(colnames(dfRIc[["paramTest0"]][['RI0.05.csv']]),
       meanDataBinary[[paste('RI',ri,sep='')]],type='p')
  
  # plot(colnames(dfRIc[["paramTest0"]][['RI0.05.csv']]),
  #      meanDataTimes[[paste('RI',ri,sep='')]],
  #      main = paste('RandomInit=',as.character(ri),sep = ''),sub='Averaged data Times', xlab='c', ylab='probability',
  #      type='p', col='blue',pch=20,lty=1)
  par(new=T)
}

ggplot(meanDataBinary[['RI0.05']], aes(x=colnames(meanDataBinary[['RI0.05']]), y=meanDataBinary[['RI0.05']]))



