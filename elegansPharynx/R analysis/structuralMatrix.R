library(igraph)
library(dplyr)
library(ggplot2)
setwd("~/elegansProject/elegansPharynx/R analysis")


# First, prepare network attributes with the entire connectome
original_edgelist <- read.csv("hermPharynx_connections.csv", stringsAsFactors = FALSE)
original_nodelist <- read.csv("1.2cell_typesPharynx.csv", stringsAsFactors = FALSE)


# Create iGraph object and calculate network properties
graph <- graph.data.frame(original_edgelist, directed = TRUE, vertices = original_nodelist)

V(graph)$degree <- degree(graph)
V(graph)$closeness <- centralization.closeness(graph)$res
V(graph)$betweenness <- centralization.betweenness(graph)$res
V(graph)$eigen <- centralization.evcent(graph)$vector


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
V(graph)$community=cfg$membership
colrs <- adjustcolor( c("gray50", "tomato", "gold", "yellowgreen"), alpha=.6)
plot(netSimply, vertex.color=colrs[V(netSimply)$community])
    # K-core decomposition
kc=coreness(netSimply,mode='all')
plot(netSimply,vertex.size=kc*6, vertex.label=kc)


# Generate dataframe for nodes with updated network attributes, and ordered by community
nodes=get.data.frame(graph, what='vertices')
nodes_ordered = nodes[order(node_list$community),] 
all_nodes = nodes_ordered$name

# Prepare plotting with separate graphs for electrical and chemical connections
chemConn = read.csv("hermPharynx_connectionsCHEM.csv", stringsAsFactors = FALSE)
elecConn = read.csv("hermPharynx_connectionsELEC.csv", stringsAsFactors = FALSE)


# Create iGraph object
chemGraph = graph.data.frame(chemConn, directed = TRUE, vertices = nodes)
elecGraph = graph.data.frame(elecConn, directed = T, vertices = nodes)


# Determine a community for each edge. If two nodes belong to the same community, label the edge with that community. 
# If not, the edge community value is 'NA'
edgesChem = get.data.frame(chemGraph, what = "edges") %>% 
  inner_join(node_list %>% select(name, community), by = c("from" = "name")) %>%
  inner_join(node_list %>% select(name, community), by = c("to" = "name")) %>%
   mutate(group = ifelse(community.x == community.y, community.x, NA) %>% factor())

edgesElec = get.data.frame(elecGraph, what = "edges") %>% 
  inner_join(node_list %>% select(name, community), by = c("from" = "name")) %>%
  inner_join(node_list %>% select(name, community), by = c("to" = "name")) %>%
  mutate(group = ifelse(community.x == community.y, community.x, NA) %>% factor())


# Adjust the 'to' and 'from' factor levels so they are equal
# to this complete list of node names
plot_data = edgesChem %>% mutate(
  to = factor(to, levels = all_nodes),
  from = factor(from, levels = all_nodes))

# Create the adjacency matrix plot
ggplot(plot_data, aes(x = from, y = to, color=group)) +
  geom_point(shape=18, size=4) +
  geom_point(data = edgesElec, aes(x=from, y=to), color='grey19')+
  theme_bw() +
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
  


