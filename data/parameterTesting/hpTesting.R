

filenames=list.files('hpData', full.names = FALSE)

hpTest=list()
meanhp=list()

for (file in filenames){
  hpTest[[file]]=read.csv(paste('hpData/',file, sep = ''), check.names = FALSE)
  
  for (i in colnames(hpTest[[file]])){
    meanhp[[file]][[i]]=mean(hpTest[[file]][[i]])
  }
  
  plot(colnames(hpTest[[file]]), meanhp[[file]], main = paste(substr(file,9,9),'=',substr(file,10,12),sep=' '),
       xlab = 'hiperpolarization value', ylab = 'probability rrp2spike')        
 
}



