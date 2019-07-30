setwd("~/elegansProject/elegansSomatic/R - conn/")
library(igraph)
library(dplyr)
library(ggplot2)
library(expss)

######### Prepare Structural connectivity matrices ---------------
# First, prepare network attributes with the entire connectome
original_edgelist <- read.csv("2.1hermSomatic_connections.csv", stringsAsFactors = FALSE)
original_nodelist <- read.csv("1.2cell_typesSomatic.csv", stringsAsFactors = FALSE)

# Create iGraph object 
graph <- graph.data.frame(original_edgelist, directed = TRUE, vertices = original_nodelist)
rm (original_edgelist, original_nodelist)

# Calculate network properties
V(graph)$degree <- degree(graph)
V(graph)$closeness <- centralization.closeness(graph)$res
V(graph)$betweenness <- centralization.betweenness(graph)$res
V(graph)$eigen <- centralization.evcent(graph)$vector

# Generate dataframe for nodes ordered by group w\ properties
nodes=get.data.frame(graph, what='vertices')
nodes_ordered = nodes[order(nodes$group),]   ## groups based on cell type as in: elegansSomatic/simulator/data/networksetup/cell_typesSomatic.csv 
all_nodes = nodes_ordered$name
rm (nodes_ordered)

# Determine group for each edge. If two nodes belong to the same cell type group, 
# label the edge with that group. If not, the edge group value is 'NA'.
edges = get.data.frame(graph, what = "edges") %>%
  inner_join(nodes %>% select(name, group), by = c("from" = "name")) %>%
  inner_join(nodes %>% select(name, group), by = c("to" = "name")) %>%
  mutate(group = ifelse(group.x == group.y, group.x, NA) %>% factor())

# Adjust the 'to' and 'from' factor levels so they are equal
# to this complete list of node names
edges = edges %>% mutate(
  to = factor(to, levels = all_nodes),
  from = factor(from, levels = all_nodes))

# Generate variable with inh/exc structural weights
edges$WxSGN=edges$Weight*edges$exin
edges$lWxSGN=edges$logWeight*edges$exin

edges$Weight=NULL
edges$logWeight=NULL

######## Prepare Functional connectivity matrices -----
fConn <- read.csv("fConnSomatic.csv", stringsAsFactors = FALSE)

# Create iGraph for functional connectivity data
fGraph = graph.data.frame(fConn, directed = TRUE, vertices = nodes)

# Determine a group for each edge. If two nodes belong to the same group,  
# label the edge with that group. If not, the edge group value is 'NA'.
edgesF = get.data.frame(fGraph, what = "edges") %>%
  inner_join(nodes %>% select(name, group), by = c("from" = "name")) %>%
  inner_join(nodes %>% select(name, group), by = c("to" = "name")) %>%
  mutate(group = ifelse(group.x == group.y, group.x, NA) %>% factor())

edgesF$group.x=NULL
edgesF$group.y=NULL

# Adjust the 'to' and 'from' factor levels so they are equal
# to this complete list of node names
edgesF = edgesF %>% mutate(
  to = factor(to, levels = all_nodes),
  from = factor(from, levels = all_nodes))


######### Preparing merged dataframe -----
# First, remove unuseful variables from edgesF and create new SFdf
# SFdf=edgesF
# 
# # Add structural weights ordered by connection.
# # Optimization: vectorialization, preallocation and use which()
# SFdf$strucWChem=integer(nrow(SFdf))
# SFdf$strucWElec=integer(nrow(SFdf))
# 
# for (n in 1:length(all_nodes)){
#   rlSFdf=which(SFdf$from==all_nodes[n])
#   rledges=which(edges$from==all_nodes[n])
#   print(n)
#   for (connc in rledges){
#     print(connc)
#     for (connf in rlSFdf){
#       if (SFdf$to[connf]==edges$to[connc] & edges$Syn[connc]=='chemical'){
#         SFdf$strucWChem[connf]=edges$WxSGN[connc]}
#       if (SFdf$to[connf]==edges$to[connc] & edges$Syn[connc]=='electrical'){
#         SFdf$strucWElec[connf]=edges$WxSGN[connc]}
#     }
#   }
# }
# rm(connc,connf,n,rledges,rlSFdf)
#write.csv(SFdf, 'SFdf.csv', row.names=FALSE)

## The process take about 20 minutes. I saved result and load from there. 
SFdf=read.csv('SFdf.csv')

## Sum up electrical and chemical structural weights. 
## Functional weights does not differentiate among them.
SFdf$sumEC=SFdf$strucWChem+SFdf$strucWElec
SFdf$logsumEC=1+log(abs(SFdf$sumEC))
SFdf$logsumEC[SFdf$logsumEC==-Inf]=0
SFdf$logsumEC[SFdf$sumEC<0]=SFdf$logsumEC[SFdf$sumEC<0]*-1

## Create a new dataframe without self connectivity
SFdf1=SFdf
SFdf1$connPhi[SFdf1$from==SFdf1$to]=NA
subset=SFdf1$connPhi
SFdf1=SFdf1[complete.cases(subset), ]
rm(subset)


##### Analyzing categorical existence of connection between neurons. ----
## Categorical variable for structural connections
SFdf1$catE[SFdf1$logsumEC>0]=1
SFdf1$catE[SFdf1$logsumEC==0]=0
SFdf1$catE[SFdf1$logsumEC<0]=-1

## labels to variables
SFdf1=apply_labels(SFdf1, connPsi1='Functional connections w/o FDR', 
                  connPsi1=c('Positive\ncorrelation'=1,'Negative\ncorrelation'=-1, 'Null'=0), 
                  connPsi2='Functional connections w/ FDR',
                  connPsi2=c('Positive\ncorrelation'=1,'Negative\ncorrelation'=-1, 'Null'=0),
                  catE='Structural connections',
                  catE=c('Excitatory'=1,'Inhibitory'=-1, 'Non-Existent'=0))


####### with Psi1
cro(SFdf1$connPsi1, list(SFdf1$catE,total()))
addmargins(prop.table(table(SFdf1$connPsi1, SFdf1$catE), margin=2))


##Sensitivity (i.e. rate of true positives: TP/TP+FN) and specificity (i.e. rate of true negatives: TN/TN+FP)
##for predicting excitatory, inhibitory and non-existant connections.
SensitivityPsi1EXC=length(SFdf1$connPsi1[SFdf1$connPsi1==1&SFdf1$catE==1])/length(SFdf1$catE[SFdf1$catE==1])
SpecificityPsi1EXC=length(SFdf1$catE[SFdf1$connPsi1<=0&SFdf1$catE<=0])/length(SFdf1$catE[SFdf1$catE<=0])

SensitivityPsi1INH=length(SFdf1$connPsi1[SFdf1$connPsi1==-1&SFdf1$catE==-1])/length(SFdf1$catE[SFdf1$catE==-1])
SpecificityPsi1INH=length(SFdf1$catE[SFdf1$connPsi1>=0&SFdf1$catE>=0])/length(SFdf1$catE[SFdf1$catE>=0])

SensitivityPsi1NULL=length(SFdf1$connPsi1[SFdf1$connPsi1==0&SFdf1$catE==0])/length(SFdf1$catE[SFdf1$catE==0])
SpecificityPsi1NULL=length(SFdf1$catE[SFdf1$connPsi1!=0&SFdf1$catE!=0])/length(SFdf1$catE[SFdf1$catE!=0])


chisq.test(SFdf1$connPsi1, SFdf1$catE)



####### with Psi2
cro(SFdf1$connPsi2, list(SFdf1$catE,total()))
addmargins(prop.table(table(SFdf1$connPsi2, SFdf1$catE)))

##Sensitivity (i.e. rate of true positives: TP/TP+FN) and specificity (i.e. rate of true negatives: TN/TN+FP)
##for predicting excitatory, inhibitory and non-existant connections.
SensitivityPsi2EXC=length(SFdf1$connPsi2[SFdf1$connPsi2==1&SFdf1$catE==1])/length(SFdf1$catE[SFdf1$catE==1])
SpecificityPsi2EXC=length(SFdf1$catE[SFdf1$connPsi2<=0&SFdf1$catE<=0])/length(SFdf1$catE[SFdf1$catE<=0])

SensitivityPsi2INH=length(SFdf1$connPsi2[SFdf1$connPsi2==-1&SFdf1$catE==-1])/length(SFdf1$catE[SFdf1$catE==-1])
SpecificityPsi2INH=length(SFdf1$catE[SFdf1$connPsi2>=0&SFdf1$catE>=0])/length(SFdf1$catE[SFdf1$catE>=0])

SensitivityPsi2NULL=length(SFdf1$connPsi2[SFdf1$connPsi2==0&SFdf1$catE==0])/length(SFdf1$catE[SFdf1$catE==0])
SpecificityPsi2NULL=length(SFdf1$catE[SFdf1$connPsi2!=0&SFdf1$catE!=0])/length(SFdf1$catE[SFdf1$catE!=0])


chisq.test(SFdf1$connPsi2,SFdf1$catE)


## Differential analysis for ELECTRICAL synapses
## Prepare dataframe
SFdfE=SFdf1
SFdfE$strucWElec[SFdfE$strucWChem>0&SFdfE$strucWElec==0]=NA ## filtering electrical synapses + no connection
subset=SFdfE$strucWElec
SFdfE=SFdfE[complete.cases(subset), ]
rm(subset)

cro(SFdfE$connPsi1, list(SFdfE$catE,total()))
addmargins(prop.table(table(SFdfE$connPsi1, SFdfE$catE), margin=2))

EsensPsi2EXC=length(SFdfE$connPsi2[SFdfE$connPsi2==1&SFdfE$catE==1])/length(SFdfE$catE[SFdfE$catE==1])
EspecPsi2EXC=length(SFdfE$catE[SFdfE$connPsi2<=0&SFdfE$catE<=0])/length(SFdfE$catE[SFdfE$catE<=0])

EsensPsi2INH=length(SFdfE$connPsi2[SFdfE$connPsi2==-1&SFdfE$catE==-1])/length(SFdfE$catE[SFdfE$catE==-1])
EspecPsi2INH=length(SFdfE$catE[SFdfE$connPsi2>=0&SFdfE$catE>=0])/length(SFdfE$catE[SFdfE$catE>=0])

EsensPsi2NULL=length(SFdfE$connPsi2[SFdfE$connPsi2==0&SFdfE$catE==0])/length(SFdfE$catE[SFdfE$catE==0])
EspecPsi2NULL=length(SFdfE$catE[SFdfE$connPsi2!=0&SFdfE$catE!=0])/length(SFdfE$catE[SFdfE$catE!=0])

chisq.test(SFdfE$connPsi2,SFdfE$catE)


## Differential analysis for CHEMICAL synapses
## Prepare dataframe
SFdfC=SFdf1
SFdfC$strucWChem[SFdfC$strucWElec>0&SFdfC$strucWChem==0]=NA ## filtering electrical synapses + no connection
subset=SFdfC$strucWChem
SFdfC=SFdfC[complete.cases(subset), ]
rm(subset)

cro(SFdfC$connPsi1, list(SFdfC$catE,total()))
addmargins(prop.table(table(SFdfC$connPsi1, SFdfC$catE), margin=2))

CsensPsi2EXC=length(SFdfC$connPsi2[SFdfC$connPsi2==1&SFdfC$catE==1])/length(SFdfC$catE[SFdfC$catE==1])
CspecPsi2EXC=length(SFdfC$catE[SFdfC$connPsi2<=0&SFdfC$catE<=0])/length(SFdfC$catE[SFdfC$catE<=0])

CsensPsi2INH=length(SFdfC$connPsi2[SFdfC$connPsi2==-1&SFdfC$catE==-1])/length(SFdfC$catE[SFdfC$catE==-1])
CspecPsi2INH=length(SFdfC$catE[SFdfC$connPsi2>=0&SFdfC$catE>=0])/length(SFdfC$catE[SFdfC$catE>=0])

CsensPsi2NULL=length(SFdfC$connPsi2[SFdfC$connPsi2==0&SFdfC$catE==0])/length(SFdfC$catE[SFdfC$catE==0])
CspecPsi2NULL=length(SFdfC$catE[SFdfC$connPsi2!=0&SFdfC$catE!=0])/length(SFdfC$catE[SFdfC$catE!=0])

chisq.test(SFdfC$connPsi2,SFdfC$catE)


### Use the best Psi predictor to eliminate non significant functional connectivity weights

SensitivityPsi1EXC   #Better1
SensitivityPsi2EXC

SensitivityPsi1INH   #Better1
SensitivityPsi2INH

SensitivityPsi1NULL
SensitivityPsi2NULL  #Better2

SpecificityPsi1EXC
SpecificityPsi2EXC   #Better2

SpecificityPsi1INH
SpecificityPsi2INH   #Better2

SpecificityPsi1NULL  #Better1
SpecificityPsi2NULL


SFdf$connPhiPsi=SFdf$connPhi
SFdf$connPhiPsi[SFdf$connPsi2==0]=0
SFdf1$connPhiPsi=SFdf1$connPhi
SFdf1$connPhiPsi[SFdf1$connPsi2==0]=0



#### Analyzing weight correlations between functional and structural networks ----
# Filter for structural existent connections
SFdf2=SFdf1
SFdf2$logsumEC[SFdf2$logsumEC==0]=NA ## filtering structural inexistent
subset=SFdf2$logsumEC
SFdf2=SFdf2[complete.cases(subset), ]
SFdf2$connPhiPsi[SFdf2$connPhiPsi==0]=NA ## filtering functional Null
SFdf2$connPhiPsi[SFdf2$logsumEC>0&SFdf2$connPhiPsi<0]=NA   ## Filtering excitatory true positives
SFdf2$connPhiPsi[SFdf2$logsumEC<0&SFdf2$connPhiPsi>0]=NA   ## Filtering inhibitory true positives
subset=SFdf2$connPhiPsi
SFdf2=SFdf2[complete.cases(subset), ]
rm(subset)

# Pearson correlation test
cor.test(SFdf2$connPhiPsi, SFdf2$logsumEC, method=c("pearson"))
# Plot correlation
ggplot(SFdf2, aes(logsumEC, connPhiPsi))+
  geom_point(size=0.5)+
  geom_smooth(method='lm',formula=y~x, size=0.5)+
  xlab('Structural Weight')+
  ylab('Functional Weight')+
  ggtitle('Weight correlation - Somatic')


## Independent analysis for Excitatory synapses
SFdf2Exc=SFdf2
SFdf2Exc$connPhiPsi[SFdf2Exc$connPhiPsi<0]=NA
subset=SFdf2Exc$connPhiPsi
SFdf2Exc=SFdf2Exc[complete.cases(subset), ]
rm(subset)

# Pearson correlation test
cor.test(SFdf2Exc$connPhiPsi, SFdf2Exc$logsumEC, method=c("pearson"))
# Plot correlation
ggplot(SFdf2Exc, aes(logsumEC, connPhiPsi))+
  geom_point(size=0.5)+
  geom_smooth(method='lm',formula=y~x, size=0.5)+
  xlab('Structural Weight')+
  ylab('Functional Weight')+
  ggtitle('Weight correlation for excitatory synapses - Somatic')


## Independent analysis for Inhibitory synapses
SFdf2Inh=SFdf2
SFdf2Inh$connPhiPsi[SFdf2Inh$connPhiPsi>0]=NA
subset=SFdf2Inh$connPhiPsi
SFdf2Inh=SFdf2Inh[complete.cases(subset), ]
rm(subset)

# Pearson correlation test
cor.test(SFdf2Inh$connPhiPsi, SFdf2Inh$logsumEC, method=c("pearson"))
# Plot correlation
ggplot(SFdf2Inh, aes(logsumEC, connPhiPsi))+
  geom_point(size=0.5)+
  geom_smooth(method='lm',formula=y~x, size=0.5)+
  xlab('Structural Weight')+
  ylab('Functional Weight')+
  ggtitle('Weight correlation for excitatory synapses - Somatic')


### Weight correlations with electrical weights and excitatory connections
SFdfE=SFdf2Exc
SFdfE$strucWElec[SFdfE$strucWElec==0]=NA ## filtering electrical synapses
subset=SFdfE$strucWElec
SFdfE=SFdfE[complete.cases(subset), ]
rm(subset)
# Pearson correlation test
cor.test(SFdfE$connPhiPsi, SFdfE$strucWElec, method=c("pearson"))

# Plot correlation
ggplot(SFdfE, aes(strucWElec, connPhiPsi))+
  geom_point(size=0.5)+
  geom_smooth(method='lm',formula=y~x, size=0.5)+
  xlab('Structural Weight')+
  ylab('Functional Weight')+
  ggtitle('Weight correlation electrical - Somatic')


### Weight correlations with electrical weights and inhibitory connections
## Prepare dataframe
SFdfE=SFdf2Inh
SFdfE$strucWElec[SFdfE$strucWElec==0]=NA ## filtering electrical synapses
subset=SFdfE$strucWElec
SFdfE=SFdfE[complete.cases(subset), ]
rm(subset)
# Pearson correlation test
cor.test(SFdfE$connPhiPsi, SFdfE$strucWElec, method=c("pearson"))

# Plot correlation
ggplot(SFdfE, aes(strucWElec, connPhiPsi))+
  geom_point(size=0.5)+
  geom_smooth(method='lm',formula=y~x, size=0.5)+
  xlab('Structural Weight')+
  ylab('Functional Weight')+
  ggtitle('Weight correlation electrical - Somatic')


### Weight correlations with chemical weights and excitatory synapses
## Prepare dataframe
SFdfC=SFdf2Exc
SFdfC$strucWChem[SFdfC$strucWChem==0]=NA ## filtering chemical synapses      
subset=SFdfC$strucWChem
SFdfC=SFdfC[complete.cases(subset), ]
rm(subset)

# Pearson correlation test
cor.test(SFdfC$connPhiPsi, SFdfC$strucWChem, method=c("pearson"))

# Plot correlation
ggplot(SFdfC, aes(strucWChem, connPhiPsi))+
  geom_point(size=0.5)+
  geom_smooth(method='lm',formula=y~x, size=0.5)+
  xlab('Structural Weight')+
  ylab('Functional Weight')+
  ggtitle('Weight correlation chemical - Somatic')


### Weight correlations with chemical weights and inhibitory synapses
SFdfC=SFdf2Inh
SFdfC$strucWChem[SFdfC$strucWChem==0]=NA ## filtering chemical synapses      
subset=SFdfC$strucWChem
SFdfC=SFdfC[complete.cases(subset), ]
rm(subset)

# Pearson correlation test
cor.test(SFdfC$connPhiPsi, SFdfC$strucWChem, method=c("pearson"))

# Plot correlation
ggplot(SFdfC, aes(strucWChem, connPhiPsi))+
  geom_point(size=0.5)+
  geom_smooth(method='lm',formula=y~x, size=0.5)+
  xlab('Structural Weight')+
  ylab('Functional Weight')+
  ggtitle('Weight correlation chemical - Somatic')


#### Plotting ----------
## Create structural adjacency matrix showing communities
ggplot(edges, aes(x = from, y = to, group=Syn, color=group, shape=Syn)) +
  geom_point(alpha=0.5, size=0.7)+
  geom_hline(yintercept =c(68.5, 78.5, 145.5, 167.5, 173.5, 196.5), alpha=0.2)+
  geom_vline(xintercept =c(68.5, 78.5, 145.5, 167.5, 173.5, 196.5), alpha=0.2)+
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  labs(colour='Group', shape='Synapse type')+
  scale_color_discrete(labels=c('Sensory','Sensory-Interneuron','Interneuron','Sensory-Motor','Sensory-Motor-Interneuron','Motor-Interneuron','Motor'))+
  ggtitle('Structural connectivity matrix - Somatic')+
  theme(
    axis.text.x = element_blank(),
    axis.text.y = element_blank(),
    axis.ticks = element_blank(),
    # Force the plot into a square aspect ratio
    aspect.ratio = 1,
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank())

## Create structural adjacency matrix showing weights
ggplot(edges, aes(x = from, y = to, group=Syn, color=lWxSGN, shape=Syn)) +
  geom_point(alpha=0.9, size=0.9)+
  geom_hline(yintercept =c(68.5, 78.5, 145.5, 167.5, 173.5, 196.5), alpha=0.2)+
  geom_vline(xintercept =c(68.5, 78.5, 145.5, 167.5, 173.5, 196.5), alpha=0.2)+
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  labs(colour='Connection\nweight', shape='Synapse type')+
  scale_colour_gradient2(low = 'midnightblue', high = 'indianred' )+
  ggtitle('Structural connectivity matrix - Somatic')+
  theme(
    legend.title.align = 0.5,
    axis.text.x = element_blank(),
    axis.text.y = element_blank(),
    axis.ticks = element_blank(),
    # Force the plot into a square aspect ratio
    aspect.ratio = 1,
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank())


## Functional connectivity matrix
ggplot(SFdf, aes(x = from, y = to, color=connPhiPsi)) +
  geom_point(shape=15) +
  geom_hline(yintercept =c(68.5, 78.5, 145.5, 167.5, 173.5, 196.5), alpha=0.05)+
  geom_vline(xintercept =c(68.5, 78.5, 145.5, 167.5, 173.5, 196.5), alpha=0.05)+
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  labs(colour='Functional\nweight')+
  ggtitle('Functional connectivity matrix - Somatic')+
  scale_colour_gradient2(low = 'aquamarine3', high = 'chocolate1')+
  theme(
    legend.title.align = 0.5,
    axis.text.x = element_blank(),
    axis.text.y = element_blank(),
    axis.ticks = element_blank(),
    # Force the plot into a square aspect ratio
    aspect.ratio = 1,
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank())

## Functional matrix w/o sefl connections
ggplot(SFdf1, aes(x = from, y = to, color=connPhiPsi)) +
  geom_point(shape=15, size=6, alpha=0.8) +
  geom_hline(yintercept =c(68.5, 78.5, 145.5, 167.5, 173.5, 196.5), alpha=0.2)+
  geom_vline(xintercept =c(68.5, 78.5, 145.5, 167.5, 173.5, 196.5), alpha=0.2)+
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  labs(colour='Functional\nweight')+
  ggtitle('Functional connectivity matrix w/o self conn. - Somatic')+
  scale_colour_gradient2(low = 'aquamarine3', high = 'chocolate1')+
  theme(
    legend.title.align = 0.5,
    axis.text.x = element_blank(),
    axis.text.y = element_blank(),
    axis.ticks = element_blank(),
    # Force the plot into a square aspect ratio
    aspect.ratio = 1)

## Functional matrix w/o sefl connections logarithmic tranformation
SFdf1$logPhiPsi=log(abs(SFdf1$connPhiPsi))
SFdf1$logPhiPsi[SFdf1$logPhiPsi==-Inf]=0
SFdf1$logPhiPsi[SFdf1$connPhiPsi<0]=SFdf1$logPhiPsi[SFdf1$connPhiPsi<0]*-1


ggplot(SFdf1, aes(x = from, y = to, color=logPhiPsi)) +
  geom_point(shape=3, size=0.2) +
  geom_hline(yintercept =c(68.5, 78.5, 145.5, 167.5, 173.5, 196.5), alpha=0.2)+
  geom_vline(xintercept =c(68.5, 78.5, 145.5, 167.5, 173.5, 196.5), alpha=0.2)+
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  labs(colour='Functional\nweight')+
  ggtitle('Functional connectivity matrix w/o self conn. - Somatic')+
  scale_colour_gradient2(low = 'aquamarine3', high = 'chocolate1')+
  theme(
    legend.title.align = 0.5,
    axis.text.x = element_blank(),
    axis.text.y = element_blank(),
    axis.ticks = element_blank(),
    # Force the plot into a square aspect ratio
    aspect.ratio = 1,
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank())



#########  Structural and functional matrices -----
# ggplot() +
#   geom_point(data = SFdf1, aes(x=from, y=to, colour=connPhiPsi), shape=15, size=5, alpha=0.8)+
#   geom_point(data = edges, aes(x = from, y = to, group=Syn, shape=Syn), alpha=0.2)+
#   theme_light() +
#   scale_colour_gradient2(low = 'lightcyan2', high = 'darkorange1')+
#   ggtitle('Structural & Functional matrix - Somatic')+
#   theme(
#     # Rotate the x-axis lables so they are legible
#     axis.text.x = element_text(angle = 270, hjust = 0),
#     # Force the plot into a square aspect ratio
#     aspect.ratio = 1)
