setwd("~/elegansProject/elegansPharynx/R - conn")
library(igraph)
library(dplyr)
library(ggplot2)
library(expss)

######### Prepare Structural connectivity matrices ---------------
# First, prepare network attributes with the entire connectome
original_edgelist <- read.csv("2.1hermPharynx_connections.csv", stringsAsFactors = FALSE)
original_nodelist <- read.csv("1.2cell_typesPharynx.csv", stringsAsFactors = FALSE)

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
nodes_ordered = nodes[order(nodes$group),]   ## groups based on cell type as in: elegansPharynx/simulator/data/networksetup/cell_typesPharynx.csv 
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
fConn <- read.csv("fConn.csv", stringsAsFactors = FALSE)

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
SFdf=edgesF

# Add structural weights ordered by connection.
# Optimization: vectorialization, preallocation and use which()
SFdf$strucWChem=integer(nrow(SFdf))
SFdf$strucWElec=integer(nrow(SFdf))

for (n in 1:length(all_nodes)){
  rlSFdf=which(SFdf$from==all_nodes[n])
  rledges=which(edges$from==all_nodes[n])
  print(n)
  for (connc in rledges){
    print(connc)
    for (connf in rlSFdf){
      if (SFdf$to[connf]==edges$to[connc] & edges$Syn[connc]=='chemical'){
        SFdf$strucWChem[connf]=edges$WxSGN[connc]}
      if (SFdf$to[connf]==edges$to[connc] & edges$Syn[connc]=='electrical'){
        SFdf$strucWElec[connf]=edges$WxSGN[connc]}
    }
  }
}

rm(connc,connf,n,rledges,rlSFdf)

## Sum up electrical and chemical structural weights. 
## Functional weights does not differentiate among them.
SFdf$sumEC=SFdf$strucWChem+SFdf$strucWElec
SFdf$logsumEC=1+log(SFdf$sumEC)
SFdf$logsumEC[SFdf$logsumEC==-Inf]=0

## Log for chemical and electrical weights
SFdf$strucWChem=log(SFdf$strucWChem+1)
SFdf$strucWElec=log(SFdf$strucWElec+1)

## Create a new dataframe without self connectivity
SFdf1=SFdf
SFdf1$connPhi[SFdf1$from==SFdf1$to]=NA
subset=SFdf1$connPhi
SFdf1=SFdf1[complete.cases(subset), ]
rm(subset)

##### Analyzing categorical existence of connection between neurons. ----
## Categorical variable for structural connections
SFdf1$catE[SFdf1$sumEC>0]=1
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

##Sensitivity and specificity just for excitatory connections as Pharynx doesnt have inhibitory.
# Sensitivity of GC to predict structural excitatory connections 
#(i.e. rate of true positives: TP/TP+FN)
SensitivityPsi1=sum(SFdf1$connPsi1[SFdf1$connPsi1==1&SFdf1$catE==1])/sum(SFdf1$catE[SFdf1$catE==1])
SensitivityPsi1
# Specificity of GC to predict absent structural connecitons 
#(i.e. rate of true negatives: TN/TN+FP)
SpecificityPsi1=abs(length(SFdf1$catE[SFdf1$connPsi1<=0&SFdf1$catE<=0]))/length(SFdf1$catE[SFdf1$catE<=0])
SpecificityPsi1

chisq.test(SFdf1$connPsi1, SFdf1$catE)

ggplot(SFdf1, aes(as.factor(catE), fill=as.factor(connPsi1)))+
  geom_bar(width = 0.8)+
  scale_fill_hue(direction = -1, h.start=90)+
  xlab('Structural')+
  labs(fill="Functional")+
  ggtitle('Categorical predictions w/o FDR - Pharynx')


####### with Psi2
cro(SFdf1$connPsi2, list(SFdf1$catE,total()))
addmargins(prop.table(table(SFdf1$connPsi2, SFdf1$catE)))

##Sensitivity and specificity just for excitatory connections as Pharynx doesnt have inhibitory.
# Sensitivity of GC to predict structural excitatory connections 
#(i.e. rate of true positives: TP/TP+FN)
SensitivityPsi1=sum(SFdf1$connPsi2[SFdf1$connPsi2==1&SFdf1$catE==1])/sum(SFdf1$catE[SFdf1$catE==1])
SensitivityPsi1
# Specificity of GC to predict absent structural connecitons 
#(i.e. rate of true negatives: TN/TN+FP)
SpecificityPsi1=abs(length(SFdf1$catE[SFdf1$connPsi2<=0&SFdf1$catE<=0]))/length(SFdf1$catE[SFdf1$catE<=0])
SpecificityPsi1

chisq.test(SFdf1$connPsi2,SFdf1$catE)

ggplot(SFdf1, aes(as.factor(catE), fill=as.factor(connPsi2)))+
  geom_bar(width = 0.8)+
  scale_fill_hue(direction = -1, h.start=90)+
  xlab('Structural')+
  labs(fill="Functional")+
  ggtitle('Categorical predictions w/ FDR - Pharynx')


## Differential analysis for ELECTRICAL synapses
## Prepare dataframe
SFdfE=SFdf1
SFdfE$strucWElec[SFdfE$strucWChem>0&SFdfE$strucWElec==0]=NA ## filtering electrical synapses + no connection
subset=SFdfE$strucWElec
SFdfE=SFdfE[complete.cases(subset), ]
rm(subset)

cro(SFdfE$connPsi1, list(SFdfE$catE,total()))
addmargins(prop.table(table(SFdfE$connPsi1, SFdfE$catE), margin=2))
#(i.e. rate of true positives: TP/TP+FN)
SensitivityPsi1=sum(SFdfE$connPsi2[SFdfE$connPsi2==1&SFdfE$catE==1])/sum(SFdfE$catE[SFdfE$catE==1])
SensitivityPsi1
# Specificity of GC to predict absent structural connecitons 
#(i.e. rate of true negatives: TN/TN+FP)
SpecificityPsi1=abs(length(SFdfE$catE[SFdfE$connPsi2<=0&SFdfE$catE<=0]))/length(SFdfE$catE[SFdfE$catE<=0])
SpecificityPsi1

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
#(i.e. rate of true positives: TP/TP+FN)
SensitivityPsi1=sum(SFdfC$connPsi2[SFdfC$connPsi2==1&SFdfC$catE==1])/sum(SFdfC$catE[SFdfC$catE==1])
SensitivityPsi1
# Specificity of GC to predict absent structural connecitons 
#(i.e. rate of true negatives: TN/TN+FP)
SpecificityPsi1=abs(length(SFdfC$catE[SFdfC$connPsi2<=0&SFdfC$catE<=0]))/length(SFdfC$catE[SFdfC$catE<=0])
SpecificityPsi1

chisq.test(SFdfC$connPsi2,SFdfC$catE)




### Use the best Psi predictor to eliminate non significant functional connectivity weights
SFdf$connPhiPsi=SFdf$connPhi
SFdf$connPhiPsi[SFdf$connPsi2==0]=NA
SFdf1$connPhiPsi=SFdf1$connPhi
SFdf1$connPhiPsi[SFdf1$connPsi2==0]=NA


### Analyzing weight correlations between functional and structural networks ----
# Filter for structural existent connections
SFdf2=SFdf1
SFdf2$logsumEC[SFdf2$logsumEC==0]=NA ## filtering first structural inexistent
subset=SFdf2$logsumEC
SFdf2=SFdf2[complete.cases(subset), ]
SFdf2$connPhiPsi[SFdf2$connPhiPsi<=0]=NA ## filtering true positives
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
  ggtitle('Weight correlation - Pharynx')

### Weight correlations with ELECTRICAL weights
## Prepare dataframe
SFdfE=SFdf1
SFdfE$strucWElec[SFdfE$strucWElec==0]=NA ## filtering electrical synapses
subset=SFdfE$strucWElec
SFdfE=SFdfE[complete.cases(subset), ]
SFdfE$strucWElec[SFdfE$connPhiPsi<=0]=NA ## filtering true positives
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
  ggtitle('Weight correlation electrical - Pharynx')

### Weight correlations with CHEMICAL weights
## Prepare dataframe
SFdfC=SFdf1
SFdfC$strucWChem[SFdfC$strucWChem==0]=NA ## filtering chemical synapses      
subset=SFdfC$strucWChem
SFdfC=SFdfC[complete.cases(subset), ]
SFdfC$strucWChem[SFdfC$connPhiPsi<=0]=NA ## filtering true positives
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
  ggtitle('Weight correlation chemical - Pharynx')


#### Plotting ----------
## Create structural adjacency matrix showing communities and weights
ggplot(edges, aes(x = from, y = to, group=Syn, color=group, shape=Syn, size=lWxSGN)) +
  geom_point(alpha=0.5)+
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  ggtitle('Structural connectivity matrix - Pharynx')+
  labs(size = "Connection weigth", colour='Group', shape='Synapse type')+
  scale_color_discrete(labels=c('Sensory-Interneuron','Sensory-Motor','Motor'))+
  theme(
    # Rotate the x-axis lables so they are legible
    axis.text.x = element_text(angle = 270, hjust = 0),
    # Force the plot into a square aspect ratio
    aspect.ratio = 1)


## NA connections as 0 to plot.
SFdf$connPhiPsi[is.na(SFdf$connPhiPsi)]=0
SFdf1$connPhiPsi[is.na(SFdf1$connPhiPsi)]=0
## Functiona matrix w/ weighted connectivity
ggplot(SFdf, aes(x = from, y = to, color=connPhiPsi)) +
  geom_point(shape=15, size=6) +
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  ggtitle('Functional connectivity matrix - Pharynx')+
  labs(colour = "Connection\nweigth")+
  scale_colour_gradient2(low = 'aquamarine3', high = 'chocolate1')+
  theme(
    legend.title.align = 0.5,
    # Rotate the x-axis lables so they are legible
    axis.text.x = element_text(angle = 270, hjust = 0),
    # Force the plot into a square aspect ratio
    aspect.ratio = 1)


## Functional matrix w/o sefl connections
ggplot(SFdf1, aes(x = from, y = to, color=connPhiPsi)) +
  geom_point(shape=15, size=6) +
  theme_light() +
  # Because we need the x and y axis to display every node,
  # not just the nodes that have connections to each other,
  # make sure that ggplot does not drop unused factor levels
  scale_x_discrete(drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  labs(colour = "Connection\nweigth")+
  ggtitle('Functional connectivity matrix w/o self conn. - Pharynx')+
  scale_colour_gradient2(low = 'aquamarine3', high = 'chocolate1')+
  theme(
    legend.title.align = 0.5,
    # Rotate the x-axis lables so they are legible
    axis.text.x = element_text(angle = 270, hjust = 0),
    # Force the plot into a square aspect ratio
    aspect.ratio = 1)


##  Structural and functional matrices
ggplot() +
  geom_point(data = SFdf1, aes(x=from, y=to, colour=connPhiPsi), shape=15, size=5, alpha=0.8)+
  geom_point(data = edges, aes(x = from, y = to, group=Syn, size=lWxSGN, shape=Syn), alpha=0.2)+
  theme_light() +
  labs(size = "Structural\nweigth", colour='Functional\nweigth', shape='Structural\nsynapse type')+
  scale_colour_gradient2(low = 'lightcyan2', high = 'darkorange1')+
  ggtitle('Structural & Functional matrix - Pharynx')+
  guides(
    size=guide_legend(order=2),
    shape=guide_legend(order=1))+
  theme(
    legend.title.align = 0.5,
    # Rotate the x-axis lables so they are legible
    axis.text.x = element_text(angle = 270, hjust = 0),
    # Force the plot into a square aspect ratio
    aspect.ratio = 1)