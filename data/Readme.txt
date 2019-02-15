Data provenance.

'.graphml' data was extracted in first place from: [check Cao's reference]. Updated with all neurons and their 3D positions from OpenWorm project: c302/NeuroML2: 'elegans.herm_onlynodes.graphml'

Edges were extracted from OpenWorm/c302/c302/data: 'herm_full_edgelist_MODIFIED.csv'. It was updated by removing edges from neurons to sensory cells and muscles: 'herm_connectome.csv'. 

Finally, .graphml is updated to 'elegans_herm.graphml' with every node and connection between neurons.

Note that some neurons found in NeuroML2 folder (VD12, VD13, MDL08) don't have connections in original 'herm_full_edgelist_MODIFIED.csv'. 


The code for the update is in 'updateEdges.py'.




