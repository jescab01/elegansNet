
## Processing data. Generate Binary and timestep dataframe.

dfTimes=list()
dfBinary=list()
probTimes=list()
probBinary=list()

foldernames=list.files('experimentalData', full.names = FALSE)

for (folder in foldernames) {
  dfnames=list.files(paste('experimentalData/',folder, sep = ''))
  dfTimes[[folder]]=list()
  dfBinary[[folder]]=list()
  probTimes[[folder]]=list()
  probBinary[[folder]]=list()
  
  
  for (n in dfnames){
    df=read.csv(paste('experimentalData/',folder,'/',n, sep=''), na.strings = 'None', check.names = FALSE)
    df[is.na(df)]=50
    
    dfTimes[[folder]][[n]]=df
    
    df[df!=50]=0
    df[df==50]=1
    dfBinary[[folder]][[n]]=df
    
    columnnames=colnames(dfTimes[[folder]][[n]])
    for (col in columnnames){
      pT=mean(dfTimes[[folder]][[n]][[col]])/50  ## max timesteps 
      probTimes[[folder]][[n]][[col]]=pT
      pB=mean(dfBinary[[folder]][[n]][[col]])
      probBinary[[folder]][[n]][[col]]=pB
      }
  }
}


## plotting 

# probabilities for success of simulation [with dfBinary data frame]
# probabilities for success of timestep [with dfTimes data frame]

RI=c(0.05,0.1,0.15,0.2)

for (ri in RI){
  for (i in 0:9){  ## How many completed tests do you have? check at dfTimes.
    plot(colnames(dfBinary[["paramTest0"]][['RI0.05.csv']]),
         probBinary[[paste('paramTest',i,sep = '')]][[paste('RI',ri,'.csv',sep='')]],
         main = paste('RandomInit=',as.character(ri),sep = ''),sub=paste('paramTest',i,'/binary',sep = ''), xlab='c', ylab='probability',
         type='p', col='blue',pch=20,lty=1)
    
    plot(colnames(dfTimes[["paramTest0"]][['RI0.05.csv']]),
         probTimes[[paste('paramTest',i,sep = '')]][[paste('RI',ri,'.csv',sep='')]],
         main = paste('RandomInit=',as.character(ri),sep = ''),sub=paste('paramTest',i,'/times',sep = ''), xlab='c', ylab='Probability',
         type='p', col='blue',pch=20,lty=1)  
  }
}


## Averaging Data -

meanDataBinary=list()
meanDataTimes=list()

for (ri in RI){
  average=((probBinary[['paramTest0']][[paste('RI',ri,'.csv',sep = '')]]+
       probBinary[['paramTest1']][[paste('RI',ri,'.csv',sep = '')]]+
       probBinary[['paramTest2']][[paste('RI',ri,'.csv',sep = '')]]+
       probBinary[['paramTest3']][[paste('RI',ri,'.csv',sep = '')]]+
       probBinary[['paramTest4']][[paste('RI',ri,'.csv',sep = '')]]+
       probBinary[['paramTest5']][[paste('RI',ri,'.csv',sep = '')]]+
       probBinary[['paramTest6']][[paste('RI',ri,'.csv',sep = '')]]+
       probBinary[['paramTest7']][[paste('RI',ri,'.csv',sep = '')]]+
       probBinary[['paramTest8']][[paste('RI',ri,'.csv',sep = '')]]+
       probBinary[['paramTest9']][[paste('RI',ri,'.csv',sep = '')]])/10)
  meanDataBinary[[paste('RI',ri,sep = '')]]=average
  
  average=((probTimes[['paramTest0']][[paste('RI',ri,'.csv',sep = '')]]+
          probTimes[['paramTest1']][[paste('RI',ri,'.csv',sep = '')]]+
          probTimes[['paramTest2']][[paste('RI',ri,'.csv',sep = '')]]+
          probTimes[['paramTest3']][[paste('RI',ri,'.csv',sep = '')]]+
          probTimes[['paramTest4']][[paste('RI',ri,'.csv',sep = '')]]+
          probTimes[['paramTest5']][[paste('RI',ri,'.csv',sep = '')]]+
          probTimes[['paramTest6']][[paste('RI',ri,'.csv',sep = '')]]+
          probTimes[['paramTest7']][[paste('RI',ri,'.csv',sep = '')]]+
          probTimes[['paramTest8']][[paste('RI',ri,'.csv',sep = '')]]+
          probTimes[['paramTest9']][[paste('RI',ri,'.csv',sep = '')]])/10)
  meanDataTimes[[paste('RI',ri,sep = '')]]=average
}


## Plotting average

for (ri in RI){
  plot(colnames(dfBinary[["paramTest0"]][['RI0.05.csv']]),
       meanDataBinary[[paste('RI',ri,sep='')]],
       main = paste('RandomInit=',as.character(ri),sep = ''),sub='Averaged data Binary', xlab='c', ylab='probability',
       type='p', col='blue',pch=20,lty=1)
  
  plot(colnames(dfBinary[["paramTest0"]][['RI0.05.csv']]),
       meanDataTimes[[paste('RI',ri,sep='')]],
       main = paste('RandomInit=',as.character(ri),sep = ''),sub='Averaged data Times', xlab='c', ylab='probability',
       type='p', col='blue',pch=20,lty=1)
}





