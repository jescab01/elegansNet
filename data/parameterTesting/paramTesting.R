dfs=list()
dform=list()

for (i in 1:get_num_sheet_in_ods('paramTests.ods')){
  df=read_ods('paramTests.ods', i)
  dfs[[i]]=df
  
  df[df!=200]=0
  df[df==200]=1
  dform[[i]]=df
}


# calculating probabilities -----------------------------------------------

## probabilities for success of simulation [with dform data frame]

pform=list()
for (a in 1:length(dform)){
  pform[[a]]=list()
  for (b in 1:ncol(dform[[a]])){
    p=mean(dform[[a]][,b])
    pform[[a]][[b]]=p
  }
}

plot(colnames(dfs[[1]]), pform[[1]], type='o', col='blue',pch=20,lty=1)



## probabilities for success of timestep [with dfs data frame]

pfs=list()
for (a in 1:length(dfs)){
  pfs[[a]]=list()
  for (b in 1:ncol(dfs[[a]])){
    p=mean(dfs[[a]][,b])/200  #Each simulation consists of 200 timesteps
    pfs[[a]][[b]]=p
  }
}

plot(colnames(dfs[[4]]), pfs[[4]], type='o', col='blue',pch=20,lty=1)

