library(igraph)
library(dplyr)
library(ggplot2)
setwd("~/elegansProject/elegansPharynx/R analysis/Connectivity")

######### Structural connectivity matrices ---------------
# First, prepare network attributes with the entire connectome
original_edgelist <- read.csv("hermPharynx_connections.csv", stringsAsFactors = FALSE)
original_nodelist <- read.csv("1.2cell_typesPharynx.csv", stringsAsFactors = FALSE)


# Create iGraph object and calculate network properties
graph <- graph.data.frame(original_edgelist, directed = TRUE, vertices = original_nodelist)

V(graph)$degree <- degree(graph)
V(graph)$closeness <- centralization.closeness(graph)$res
V(graph)$betweenness <- centralization.betweenness(graph)$res
V(graph)$eigen <- centralization.evcent(graph)$vector

rm (original_edgelist, original_nodelist)


# Generate an undirected graph to calculate communities (add the most appropriate calculation 
# to node as attribute (i.e. V(graph)$community=cfg$membership))
netSimply=as.undirected(graph, mode='collapse',edge.attr.comb=list(weight='sum','ignore'))

   # Based on Edge betweeness (Newman-Girvan)
ceb=cluster_edge_betweenness(netSimply)
dendPlot(ceb, mode = 'hclust')
plot(ceb,netSimply)
    # Based on propagating labels
clp=cluster_label_prop(netSimply)
plot(clp, netSimply)
    # Based on greedy optimization of modularity
cfg=cluster_fast_greedy(netSimply)
plot(cfg, netSimply)
V(netSimply)$community=cfg$membership
colrs <- adjustcolor( c("gray50", "tomato", "gold", "yellowgreen"), alpha=.6)
plot(netSimply, vertex.color=colrs[V(netSimply)$community])
    # K-core decomposition
kc=coreness(netSimply,mode='all')
plot(netSimply,vertex.size=kc*6, vertex.label=kc)

# Choose and add the most appropriate community calculation as attribute. i.e.:
V(graph)$community=cfg$membership

rm(ceb,clp,cfg,colrs,kc, netSimply)

# Generate dataframe for nodes with updated network attributes, and ordered by community/group
nodes=get.data.frame(graph, what='vertices')
#nodes_ordered = nodes[order(nodes$community),] 
nodes_ordered = nodes[order(nodes$group),] 
all_nodes = nodes_ordered$name

rm (nodes_ordered)

# Prepare plotting with separate graphs for electrical and chemical connections
chemConn = read.csv("hermPharynx_connectionsCHEM.csv", stringsAsFactors = FALSE)
elecConn = read.csv("hermPharynx_connectionsELEC.csv", stringsAsFactors = FALSE)


# Create one iGraph per network
chemGraph = graph.data.frame(chemConn, directed = TRUE, vertices = nodes)
elecGraph = graph.data.frame(elecConn, directed = T, vertices = nodes)

rm(chemConn,elecConn)

# # Determine a community for each edge. If two nodes belong to the same community, label the edge with that community. 
# # If not, the edge community value is 'NA'
# edgesChem = get.data.frame(chemGraph, what = "edges") %>% 
#   inner_join(nodes %>% select(name, community), by = c("from" = "name")) %>%
#   inner_join(nodes %>% select(name, community), by = c("to" = "name")) %>%
#    mutate(comm = ifelse(community.x == community.y, community.x, NA) %>% factor())
# 
# edgesElec = get.data.frame(elecGraph, what = "edges") %>% 
#   inner_join(nodes %>% select(name, community), by = c("from" = "name")) %>%
#   inner_join(nodes %>% select(name, community), by = c("to" = "name")) %>%
#   mutate(comm = ifelse(community.x == community.y, community.x, NA) %>% factor())


# Determine a group for each edge. If two nodes belong to the same cell type group, label the edge with that group. 
# If not, the edge group value is 'NA'
edgesChem = get.data.frame(chemGraph, what = "edges") %>% 
  inner_join(nodes %>% select(name, group), by = c("from" = "name")) %>%
  inner_join(nodes %>% select(name, group), by = c("to" = "name")) %>%
  mutate(group = ifelse(group.x == group.y, group.x, NA) %>% factor())

edgesElec = get.data.frame(elecGraph, what = "edges") %>% 
  inner_join(nodes %>% select(name, group), by = c("from" = "name")) %>%
  inner_join(nodes %>% select(name, group), by = c("to" = "name")) %>%
  mutate(group = ifelse(group.x == group.y, group.x, NA) %>% factor())



# Adjust the 'to' and 'from' factor levels so they are equal
# to this complete list of node names
edgesChem = edgesChem %>% mutate(
  to = factor(to, levels = all_nodes),
  from = factor(from, levels = all_nodes))

edgesElec = edgesElec %>% mutate(
  to = factor(to, levels = all_nodes),
  from = factor(from, levels = all_nodes))


## Create structural adjacency matrix showing communities
ggplot(edgesChem, aes(x = from, y = to, color=group)) +
  geom_point(shape=18, size=edgesChem$logWeight) +
  geom_point(data = edgesElec, aes(x=from, y=to), size=edgesElec$logWeight)+
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  theme(
    # Rotate the x-axis lables so they are legible
    axis.text.x = element_text(angle = 270, hjust = 0),
    # Force the plot into a square aspect ratio
    aspect.ratio = 1,
    # Hide the legend (optional)
    legend.position = "none")


## Create structural adjacency matrix showing weights*inh/exc 
ggplot(edgesChem, aes(x = from, y = to, color=logWeight)) +
  geom_point(shape=18, size=edgesChem$logWeight) +
  geom_point(data = edgesElec, aes(x=from, y=to), size=edgesElec$logWeight, color='grey17', alpha=0.4)+
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  scale_colour_gradient(low = 'lightgoldenrod2', high = 'orangered')+
  theme(
    # Rotate the x-axis lables so they are legible
    axis.text.x = element_text(angle = 270, hjust = 0),
    # Force the plot into a square aspect ratio
    aspect.ratio = 1,
    # Hide the legend (optional)
    legend.position = "none")



######### Functional connectivity matrices -----
fConn <- read.csv("fConn1Jul.csv", stringsAsFactors = FALSE)

# Create iGraph for functional connectivity data
fGraph = graph.data.frame(fConn, directed = TRUE, vertices = nodes)

# Determine a community for each edge. If two nodes belong to the same community, label the edge with that community. 
# If not, the edge community value is 'NA'
edgesF = get.data.frame(fGraph, what = "edges") %>% 
  inner_join(nodes %>% select(name, community), by = c("from" = "name")) %>%
  inner_join(nodes %>% select(name, community), by = c("to" = "name")) %>%
  mutate(group = ifelse(community.x == community.y, community.x, NA) %>% factor())


# Adjust the 'to' and 'from' factor levels so they are equal
# to this complete list of node names
edgesF = edgesF %>% mutate(
  to = factor(to, levels = all_nodes),
  from = factor(from, levels = all_nodes))

# prepare functional connectivity (just positive) for later
edgesF$connWeightP=pmax(0,edgesF$connWeight)
edgesF$connWxGCP=pmax(0,edgesF$connWxGC)


## Create functional adjacency matrix showing weighted connectivity
ggplot(edgesF, aes(x = from, y = to, color=connWeight)) +
  geom_point(shape=15, size=6) +
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  scale_colour_gradient2(low = 'aquamarine3', high = 'chocolate1')+
  theme(
    # Rotate the x-axis lables so they are legible
    axis.text.x = element_text(angle = 270, hjust = 0),
    # Force the plot into a square aspect ratio
    aspect.ratio = 1)


## Create functional adjacency matrix showing wighted x GC connectivity 
ggplot(edgesF, aes(x = from, y = to, color=connWxGC)) +
  geom_point(shape=15, size=6) +
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  scale_colour_gradient2(low = 'aquamarine3', high = 'chocolate1')+
  theme(
    # Rotate the x-axis lables so they are legible
    axis.text.x = element_text(angle = 270, hjust = 0),
    # Force the plot into a square aspect ratio
    aspect.ratio = 1)


######### Functional connectivity matrices (just excitatory connections)

## Create functional adjacency matrix showing Weight Positive connectivity
ggplot(edgesF, aes(x = from, y = to, color='chocolate1')) +
  geom_point(shape=15, size=edgesF$connWeightP/3) +
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  #scale_colour_gradient2(low = 'aquamarine3', high = 'chocolate1')+
  theme(
    # Rotate the x-axis lables so they are legible
    axis.text.x = element_text(angle = 270, hjust = 0),
    # Force the plot into a square aspect ratio
    aspect.ratio = 1)


## Create functional adjacency matrix showing Weight x GC Positive connectivity 
ggplot(edgesF, aes(x = from, y = to, color='chocolate1')) +
  geom_point(shape=15, size=edgesF$connWxGCP/3) +
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  #scale_colour_gradient2(low = 'aquamarine3', high = 'chocolate1')+
  theme(
    # Rotate the x-axis lables so they are legible
    axis.text.x = element_text(angle = 270, hjust = 0),
    # Force the plot into a square aspect ratio
    aspect.ratio = 1)



#########  Structural and functional matrices -----

## Structure and Weighted functional 
ggplot() +
  geom_point(data = edgesF, aes(x=from, y=to, color=connWeight), shape=15, size=7) +
  geom_point(data = edgesChem, aes(x=from, y=to), shape=18,size=edgesChem$logWeight, color='darkred')+
  geom_point(data = edgesElec, aes(x=from, y=to), size=edgesElec$logWeight, color='black', alpha=0.5)+
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  scale_color_gradient2(low = "lightcyan2", mid = "white", high = "chocolate4")+
  theme(
    # Rotate the x-axis lables so they are legible
    axis.text.x = element_text(angle = 270, hjust = 0),
    # Force the plot into a square aspect ratio
    aspect.ratio = 1)

## Structure and weighted x GC
ggplot() +
  geom_point(data = edgesF, aes(x=from,y=to, color=connWxGC), shape=15, size=7) +
  geom_point(data = edgesChem, aes(x=from, y=to), shape=18,size=edgesChem$logWeight, color='darkred')+
  geom_point(data = edgesElec, aes(x=from, y=to), size=edgesElec$logWeight, color='black', alpha=0.5)+
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  scale_color_gradient2(low = "lightcyan2", mid = "white", high = "chocolate1")+
  theme(
    # Rotate the x-axis lables so they are legible
    axis.text.x = element_text(angle = 270, hjust = 0), 
    # Force the plot into a square aspect ratio
    aspect.ratio = 1)

#####  Plot structural and functional (just excitatory) together
## Structure and weightP
ggplot() +
  geom_point(data = edgesF, aes(x=from,y=to,color=connWeightP),shape=15,size=7) +
  geom_point(data = edgesChem, aes(x=from, y=to), shape=18, size=edgesChem$logWeight, color='darkred')+
  geom_point(data = edgesElec, aes(x=from, y=to), size=edgesElec$logWeight, color='black', alpha=0.5)+
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  scale_color_gradient(low = 'white', high ='chocolate1')+
  theme(
    # Rotate the x-axis lables so they are legible
    axis.text.x = element_text(angle = 270, hjust = 0),
    # Force the plot into a square aspect ratio
    aspect.ratio = 1)

## Structure and weight x GC
ggplot() +
  geom_point(data = edgesF, aes(x=from,y=to,color=connWxGCP), shape=15, size=7) +
  geom_point(data = edgesChem, aes(x=from, y=to),shape=18, size=edgesChem$logWeight, color='darkred')+
  geom_point(data = edgesElec, aes(x=from, y=to), size=0.7, color=edgesElec$logWeight, alpha=0.5)+
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  scale_color_gradient(low = 'white', high ='chocolate1')+
  theme(
    # Rotate the x-axis lables so they are legible
    axis.text.x = element_text(angle = 270, hjust = 0),
    # Force the plot into a square aspect ratio
    aspect.ratio = 1)


######### Correlation between Structural and functional weights -----
# First, remove unuseful variables from edgesF and create new SFdf
SFdf=edgesF
SFdf$connPhi=NULL
SFdf$connPsi1=NULL
SFdf$community.x=NULL
SFdf$community.y=NULL
SFdf$group=NULL
SFdf$strucW=NA
SFdf$strucLogW=NA
SFdf$strucWe=NA
SFdf$strucLogWe=NA

# Add structural connections to SFdf organized by connection
for (connf in 1:length(SFdf$from)){
  for (connc in 1:length(edgesChem$from)){
    if (SFdf[connf,]['from']==edgesChem[connc,]['from'] & SFdf[connf,]['to']==edgesChem[connc,]['to']){
      SFdf$strucLogW[connf]=edgesChem$logWeight[connc]
      SFdf$strucW[connf]=edgesChem$Weight[connc]     
    }
  }
  for (conne in 1:length(edgesElec$from)){
    if (SFdf[connf,]['from']==edgesElec[conne,]['from'] & SFdf[connf,]['to']==edgesElec[conne,]['to']){
      SFdf$strucLogWe[connf]=edgesElec$logWeight[conne]
      SFdf$strucWe[connf]=edgesElec$Weight[conne]     
    }
  }
}


## sum up the electrical and chemical connections. Functional weight does not differentiate among them.
SFdf[is.na(SFdf)] = 0
SFdf$sumEC=SFdf$strucW+SFdf$strucWe
SFdf$logsumEC=1+log(SFdf$sumEC)
SFdf$logsumEC[SFdf$logsumEC==-Inf]=0

## generate categorical variables for structural and functional connections

for (i in 1:length(SFdf$from)){
  if (SFdf$connWxGC[i]==0){
    SFdf$catF=0
  }
  if (SFdf$connWxGC[i]<0){
    SFdf$catF=-1
  }
  if (SFdf$connWxGC[i]>0){
    SFdf$catF=1
  }
}

for (i in 1:length(SFdf$from)){
  if (SFdf$sumEC[i]==0){
    SFdf$catE=0
  }
  if (SFdf$sumEC[i]<0){
    SFdf$catE=-1
  }
  if (SFdf$sumEC[i]>0){
    SFdf$catE=1
  }
}


### Ojo! sum weight here should be aware of inhibition and excitation of neurons.
SFdf$catE[SFdf$logsumEC>0]=1
SFdf$catE[SFdf$logsumEC==0]=0
SFdf$catE[SFdf$logsumEC<0]=-1

SFdf$catF[SFdf$connWxGC>0]=1
SFdf$catF[SFdf$connWxGC==0]=-1
SFdf$catF[SFdf$connWxGC<0]=-1

SFdf$catB[SFdf$connWxGC<0 & SFdf$logsumEC<=0]=-1
SFdf$catB[SFdf$connWxGC>0 & SFdf$logsumEC>0]=1

## Examining categorical existance of connection in Structural connectome or functional one. 
table(SFdf$catF,SFdf$catE)
colSums(table(SFdf$catF,SFdf$catE))
rowSums(table(SFdf$catF,SFdf$catE))
prop.table(table(SFdf$catF,SFdf$catE))
colSums(prop.table(table(SFdf$catF,SFdf$catE)))
rowSums(prop.table(table(SFdf$catF,SFdf$catE)))

chisq.test(SFdf$catF,SFdf$catE)
fisher.test(SFdf$catF,SFdf$catE)

ggplot(SFdf, aes(catE, fill=as.factor(catF)))+
  geom_bar()

ggplot(SFdf, aes(catE, ..count..)) +
  geom_bar(aes(fill = as.factor(catF)), position = "dodge")

#Sensibility to predict structural connections

## i.e.  functional&structural==1/structural connections==1

#Especificity to predict structural conneciton

## i.e. functional&structural==0/structural==0



### Plot correlation between structural and functional weights
ggplot(SFdf, aes(logsumEC, connWeight))+
  geom_point(size=0.5)+
  geom_smooth(method='lm',formula=y~x)


ggplot(SFdf, aes(logsumEC,connWeight, colour=as.factor(catB)))+
  geom_point(size=0.5)

ggplot(SFdf, aes(logsumEC,connWeight))+
  geom_point(size=0.5, colour=as.factor(SFdf$catB+3))+
  geom_smooth(method='lm',formula=y~x, size=0.5)

### plotting weight correlation
ggplot(SFdf[SFdf$catB==1,], aes(logsumEC,connWeight))+
  geom_point(size=0.5)+
  geom_smooth(method='lm', formula=y~x)

### how are they correlating
cor.test(SFdf$connWeight, SFdf$logsumEC, method=c("pearson", "kendall", "spearman"))
