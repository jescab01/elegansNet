library(igraph)
library(dplyr)
library(ggplot2)
setwd("~/elegansProject/elegansSomatic/R analysis/Connectivity")

######### Structural connectivity matrices ---------------
# First, prepare network attributes with the entire connectome
original_edgelist <- read.csv("2.1hermSomatic_connections.csv", stringsAsFactors = FALSE)
original_nodelist <- read.csv("1.2cell_typesSomatic.csv", stringsAsFactors = FALSE)

# create iGraph
graph <- graph.data.frame(original_edgelist, directed = TRUE, vertices = original_nodelist)


## communities and network properties ----
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

## cont. -----
# Generate dataframe for nodes with updated network attributes, and ordered by community
nodes=get.data.frame(graph, what='vertices')
#nodes_ordered = nodes[order(nodes$community),] 
nodes_ordered = nodes[order(nodes$group),] 
all_nodes = nodes_ordered$name
rm (nodes_ordered)

# Determine a group for each edge. If two nodes belong to the same cell type group, label the edge with that group. 
# If not, the edge group value is 'NA'
edges = get.data.frame(graph, what = "edges") %>%
  inner_join(nodes %>% select(name, group), by = c("from" = "name")) %>%
  inner_join(nodes %>% select(name, group), by = c("to" = "name")) %>%
  mutate(group = ifelse(group.x == group.y, group.x, NA) %>% factor())

# Adjust the 'to' and 'from' factor levels so they are equal
# to this complete list of node names
edges = edges %>% mutate(
  to = factor(to, levels = all_nodes),
  from = factor(from, levels = all_nodes))

##### plotting -------
## Create structural adjacency matrix showing communities
ggplot(edges, aes(x = from, y = to, group=Syn, color=group, shape=Syn, size=Weight)) +
  geom_point(alpha=0.5)+
  geom_hline(yintercept =c(68.5, 78.5, 145.5, 167.5, 173.5, 196.5), alpha=0.08)+
  geom_vline(xintercept =c(68.5, 78.5, 145.5, 167.5, 173.5, 196.5), alpha=0.08)+
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
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank())

## Create structural adjacency matrix showing weights*inh/exc 
ggplot(edges, aes(x = from, y = to, group=Syn, color=logWxSGN, shape=Syn, size=Weight)) +
  geom_point(alpha=0.5)+
  geom_hline(yintercept =c(68.5, 78.5, 145.5, 167.5, 173.5, 196.5), alpha=0.08)+
  geom_vline(xintercept =c(68.5, 78.5, 145.5, 167.5, 173.5, 196.5), alpha=0.08)+
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  scale_colour_gradient2(low = 'skyblue', high = 'orangered')+
  theme(
    # Rotate the x-axis lables so they are legible
    axis.text.x = element_text(angle = 270, hjust = 0),
    # Force the plot into a square aspect ratio
    aspect.ratio = 1,
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank())

######### Functional connectivity matrices -----

fConn <- read.csv("fConnWonly1Jul.csv", stringsAsFactors = FALSE)

# Create iGraph for functional connectivity data
fGraph = graph.data.frame(fConn, directed = TRUE, vertices = nodes)

# Determine a community for each edge. If two nodes belong to the same community, label the edge with that community. 
# If not, the edge community value is 'NA'
edgesF = get.data.frame(fGraph, what = "edges") %>%
  inner_join(nodes %>% select(name, group), by = c("from" = "name")) %>%
  inner_join(nodes %>% select(name, group), by = c("to" = "name")) %>%
  mutate(group = ifelse(group.x == group.y, group.x, NA) %>% factor())


# Adjust the 'to' and 'from' factor levels so they are equal
# to this complete list of node names
edgesF = edgesF %>% mutate(
  to = factor(to, levels = all_nodes),
  from = factor(from, levels = all_nodes))


## Create functional adjacency matrix showing weighted connectivity
# prepare functional connectivity (just positive) for later
edgesF$connWeightP=pmax(0,edgesF$connWeight)
edgesF$connWxGCP=pmax(0,edgesF$connWxGC)

# log for positive connectivity
edgesF$logConnWP=log(edgesF$connWeightP+1)
edgesF$connWeightN=pmin(0,edgesF$connWeight)
edgesF$connWxGCN=pmin(0,edgesF$connWxGC)

# log for positive connectivity
edgesF$logConnWN=-log(-edgesF$connWeightN+1)
edgesF$logWNP=edgesF$logConnWN
edgesF$logWNP[edgesF$logWNP==0]=edgesF$logConnWP[edgesF$logWNP==0]

##variable making 0 self-connections
edgesF$lWNPnoself=edgesF$logWNP
edgesF$lWNPnoself[edgesF$from==edgesF$to]=0


##### plotting -----
ggplot(edgesF, aes(x = from, y = to, fill=lWNPnoself)) +
  geom_raster() +
  geom_hline(yintercept =c(68.5, 78.5, 145.5, 167.5, 173.5, 196.5), alpha=0.08)+
  geom_vline(xintercept =c(68.5, 78.5, 145.5, 167.5, 173.5, 196.5), alpha=0.08)+
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  scale_fill_gradient2(low = 'aquamarine3', high = 'chocolate1')+
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
ggplot(edgesF, aes(x = from, y = to, color=logConnWP)) +
  geom_point(shape=15) +
  geom_hline(yintercept =c(68.5, 78.5, 145.5, 167.5, 173.5, 196.5), alpha=0.2)+
  geom_vline(xintercept =c(68.5, 78.5, 145.5, 167.5, 173.5, 196.5), alpha=0.2)+
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  scale_colour_gradient2(low = 'white', high = 'chocolate1')+
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
  geom_raster(data = edgesF, aes(x=from, y=to, fill=lWNPnoself))+
  scale_fill_gradient2(low = 'darkseagreen', high = 'gold2')+
  geom_point(data = edges, aes(x = from, y = to, group=Syn, color=logWxSGN, shape=Syn), size=2, alpha=0.4)+
  scale_colour_gradient2(low = 'skyblue', high = 'orangered')+

  geom_hline(yintercept =c(68.5, 78.5, 145.5, 167.5, 173.5, 196.5), alpha=0.2)+
  geom_vline(xintercept =c(68.5, 78.5, 145.5, 167.5, 173.5, 196.5), alpha=0.2)+
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
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank())

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

SFdf=edgesF
SFdf$connPhi=NULL
SFdf$connPsi1=NULL
SFdf$connPsi2=NULL
SFdf$community.x=NULL
SFdf$community.y=NULL
SFdf$group=NULL
SFdf$group.x=NULL
SFdf$group.y=NULL
SFdf$connWeightP=NULL
SFdf$connWeightN=NULL
SFdf$logConnWP=NULL
SFdf$logConnWN=NULL

# add structural weights ordered by connection [save it, lots of processing resources]
# Optimization: vectorialization, preallocation and use which()
SFdf$strucW=double(nrow(SFdf))
SFdf$strucLogW=double(nrow(SFdf))

for (n in 1:length(all_nodes)){
  rlSFdf=which(SFdf$from==all_nodes[n])
  rledges=which(edges$from==all_nodes[n])
  print(n)
  for (connc in rledges){
    print(connc)
    for (connf in rlSFdf){
      if (SFdf$to[connf]==edges$to[connc]){
        SFdf$strucLogW[connf]=edges$logWxSGN[connc]
        SFdf$strucW[connf]=edges$WxSGN[connc]     
      }
    }
  }
}


write.csv(SFdf,'SFdf.csv')


### Plot and lets see..
ggplot(SFdf, aes(strucLogW, lWNPnoself))+
  geom_point(alpha=0.5)+
  geom_smooth(method='lm',formula=y~x)


### how are they correlating
cor.test(SFdf$connWeight, SFdf$strucLogW, method=c("pearson", "kendall", "spearman"))
