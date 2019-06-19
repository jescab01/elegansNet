setwd("~/elegansProject/elegansPharynx/R analysis")

edgelist <- read.csv("hermPharynx_connectionsCHEM.csv")
nodelist <- read.csv("1.2cell_typesPharynx.csv")

ConnMerged = data.frame(matrix(nrow = 0, ncol = 5))

for (s in nodelist['cell_name'][,1]){
  for (t in nodelist['cell_name'][,1]){
    for (c1 in length(edgelist[,1])){
      if (edgelist['Source'][c1,1]==s & edgelist['Target'][c1,1]==t & edgelist['Syn'][c1,1]=='chemical'){
        for (c2 in length(edgelist[,1])){
          if (edgelist['Source'][c2,1]==s & edgelist['Target'][c2,1]==t & edgelist['Syn'][c2,1]=='electrical'){
            newWeight=edgelist['Weight'][c1,1]+edgelist['Weight'][c2,1]
            connection=c(edgelist['Source'][c2,1], edgelist['Target'][c2,1], newWeight, log(newWeight, exp(1))+1, 'electricalChemical')
            ConnMerged=rbind(ConnMerged, connection)
          }
        }
      }
    }
  }
}
  