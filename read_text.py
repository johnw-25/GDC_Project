# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 15:37:33 2021

@author: jnwag
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import scipy.linalg as la

# import glumpy
# define directory to get tcga data from
root = r"C:\Users\jnwag\OneDrive\Documents\project data"
walker = os.walk(root)
list_of_dataframes = []
# step thru directory and unpack data 
for root,dirs,files in walker:
    for f in files:
        file_to_open = root + "\\" + f
        if f.endswith(".txt"):
                file = pd.read_csv(file_to_open,sep='\t',header=None)
                list_of_dataframes.append(file)
del list_of_dataframes[0]
cases = len(list_of_dataframes)
numGenes = len(file.index)
originalData = np.zeros((numGenes,cases))
for patient in range(cases):
    originalData[:, patient] = list_of_dataframes[patient][1]

genes = file[0].to_numpy()
# Begin determining intra/inter-group variability
# find variation between replicates w/ pca
pca = PCA(n_components=4) # creates PCA object
pComps = pca.fit_transform(originalData)

fig = plt.figure(figsize=(8,5))
plt.plot(pComps[:,0],pComps[:,1], 'ro')
plt.title('scree plot')
plt.xlabel('PC1')
plt.ylabel('PC2')

fig = plt.figure(figsize=(8,5))
plt.plot(pComps[:,2],pComps[:,3], 'ro')
plt.title('scree plot')
plt.xlabel('PC3')
plt.ylabel('PC4')



# plot variation explained by principal components
def VarScree(pca):
   per_var = np.round(pca.explained_variance_ratio_ * 100, decimals=1)
   labels = ['PC' + str(x) for x in range(1, len(per_var) + 1)]
   
   plt.bar(x=range(1, len(per_var) + 1), height=per_var, tick_label=labels)
   plt.ylabel('% of explained variance')
   plt.xlabel('Principal components')
   plt.title('Scree Plot')
   plt.show()

def ReduceDimensions(matrix, k):
    # This function takes an input data array and reduces it to k dimensions via SVD
    k = k-1
    
    # Compute reduced SVD
    [u, s, vh] = np.linalg.svd(matrix, full_matrices=False)
    
    # Construct diagonal sigma matrix
    s = np.diag(s)
    
    # Slice 'k' out of svd factorization
    u_k = u[:,0:k]
    s_k = s[0:k,0:k]
    v_k = vh[0:k,0:k]
    
    # Reconstruct data
    matrix_k = np.dot(u_k, np.dot(s_k,v_k))
    
    return matrix_k, u, s, vh

def ThresholdGenes(data, genes, countThreshold):
    alteredData = data[np.all(data > countThreshold, axis=1)]
    alteredGenes = genes[np.all(data > countThreshold, axis=1)]
    return alteredData, alteredGenes
        
reducedData, u, s, v = ReduceDimensions(originalData, 10)  
thresholded, new_genes = ThresholdGenes(reducedData, genes, 10)


VarScree(pca)
np.any([1,0,2,3], where=0, axis=0)

plt.figure(figsize = (10,10))
matrix = u*10000
cmap = sns.diverging_palette(135, 15, s=200, l=60, n=5, center="dark", as_cmap=True)
ax = sns.heatmap(reducedData, square=False, vmin=np.amin(matrix)/1000, vmax=np.amax(matrix)/1000, xticklabels=False, yticklabels=False, cmap=cmap)


[u, s, vh] = np.linalg.svd(np.transpose(originalData), full_matrices=False)
    
# Construct diagonal sigma matrix
s = np.diag(s)
k=9
# Slice 'k' out of svd factorization
u_k = u[:,0:k]
s_k = s[0:k,0:k]
v_k = vh[0:k,0:k]
matrix_k = np.dot(u_k, np.dot(s_k,v_k))
ax = sns.heatmap(matrix_k, square=False, vmin=np.amin(matrix)/1000, vmax=np.amax(matrix)/1000, xticklabels=False, yticklabels=False, cmap=cmap)
