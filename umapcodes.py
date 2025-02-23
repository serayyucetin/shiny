import scanpy #or import scanpy as sc
import anndata
import scipy 
import time
t0start = time.time()
import pandas
import numpy
import os
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 70
import seaborn as sns
from sklearn.decomposition import PCA

file_path = 'Hw3covid_Data_AllCells.h5ad'
if 1:  
    t0 = time.time()
    adata = scanpy.read(file_path)
    print('%.1f'%(-t0+time.time()), ' seconds passed' )
    print(type(adata.X))
    adata
    
print(adata.obs['Cell type'].unique())
print('Look at count matrix. We see integers - that confirms - data are raw-counts, not preprocessed expressions')
print(adata.X.sum(), type(adata.X), numpy.asarray(adata.X.sum(axis = 1)).ravel()[:10])
scanpy.pp.calculate_qc_metrics(adata,  percent_top=None, log1p=False, inplace=True)
scanpy.pp.filter_cells(adata, min_genes=200) # Remove cells with more than 200 and less than 8000 detected genes
scanpy.pp.filter_cells(adata, max_genes=8000) # Remove cells with more than 200 and less than 8000 detected genes

scanpy.pp.filter_genes(adata, min_cells=3) # Remove genes detected in less than 3 cells
adata
#if 0: 
#    # Remove cells with less than 5000 counts
#    adata = adata[adata.obs.n_genes_by_counts <5000, :]    
#    adata
    
scanpy.pp.normalize_total(adata, target_sum=1e4) # normalize with counts per million
scanpy.pp.log1p(adata) #take the log(1+x) of each value

if 0:
    # sc.pp.regress_out(adata, ['total_counts', 'pct_counts_mt'])
    sc.pp.regress_out(adata, ['total_counts'])

scanpy.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)

adata = adata[:, adata.var.highly_variable]

scanpy.pp.scale(adata, max_value=10) # subtract the mean expression value and divide by the standard deviation
adata
scanpy.pp.neighbors(adata, n_neighbors=10, n_pcs=40)
scanpy.tl.umap(adata)
scanpy.pl.umap(adata, color=['n_genes_by_counts', 'total_counts'])  
