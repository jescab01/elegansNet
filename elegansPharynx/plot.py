import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import pickle
import numpy as np
import seaborn as sns



with open('data/randomResults/frequencies_chem.txt', 'rb') as f:
	fq = pickle.load(f)	
'''
sns.set_style('whitegrid')
sns.kdeplot(np.array(fq.values()), bw=0.5)
sns.plt.show()
'''
density = gaussian_kde(fq.values())
xs = np.linspace(0,8,200)
density.covariance_factor = lambda : .5
density._compute_covariance()

#ploting
fig = plt.figure(figsize=(5,5))

plt.plot(xs,density(xs))

fig.suptitle('Frequency Distribution', fontsize=14)
plt.ylabel('Density')
plt.xlabel('Bandwidth = 0.5')


plt.show()