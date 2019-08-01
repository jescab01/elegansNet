elegansProject repository contains all data and coding produced by Jesus Cabrera in StefanLab. MSc project 2019 University of Edinburgh.

The project is related to the relationship between structural and functional neural networks. We compared the structural network of C. elegans reported first by White et al. (1986) with a functional network we obtained after simulating C. elegans neural activity. For computational requirements reasons we devided C. elegans network in 2 mostly independent systems -pharyngeal and somatic- so we could explore details and test algorithms in pharynx (20 neurons) and eventually apply all analysis to a huge network with (279 neurons).

Thus, the repository is devided in three directories:

	- elegansNet just for whole network simulator (python). Used to validate our system 3D 		representations in front of electrophysiological recordings.
	
	- elegansPharynx for pharyngeal system simulation (python), Granger Causality analysis (MATLAB) and data analysis (R).

	- elegansSomatic for Somatic system simulation (python), Granger Causality analysis (MATLAB) and data analysis (R).
