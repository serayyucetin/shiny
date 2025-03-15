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



def unzip_file(file_path, adata):
    if not os.path.exists(adata):
        os.makedirs(adata)
    try:
        # Attempt to open the ZIP file and extract its contents
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(adata)  # Extract all files to the specified directory
            print(f"Files extracted to {adata}")
    except Exception as e:
        print(f"An error occurred while extracting the ZIP file: {e}")
    return adata
        
def quality_cont(adata):
    scanpy.pp.calculate_qc_metrics(adata,  percent_top=None, log1p=False, inplace=True)
    print(adata.obs.columns)
    print("quality control done")
    
def filter(adata):
    scanpy.pp.filter_cells(adata, min_genes=200) # Remove cells with more than 200 and less than 8000 detected genes
    scanpy.pp.filter_cells(adata, max_genes=8000) # Remove cells with more than 200 and less than 8000 detected genes
    scanpy.pp.filter_genes(adata, min_cells=3) # Remove genes detected in less than 3 cells
    scanpy.pp.normalize_total(adata, target_sum=1e4) # normalize with counts per million
    scanpy.pp.log1p(adata) #take the log(1+x) of each value
    scanpy.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)
    adata = adata[: , adata.var.highly_variable]
    adata = adata[:10000, :]
    scanpy.pp.scale(adata, max_value=10)
    if 0:
        scanpy.pp.regress_out(adata, ['total_counts'])
    print("filtering done,moving on to clustering...")
    return adata


def cluster(adata):    
    scanpy.pp.neighbors(adata, n_neighbors=10, n_pcs=40)
    scanpy.tl.umap(adata)
    print("clustering done final plot is being processed...")
    
    
def plot(adata):
    print(adata.obs.columns)
    if 'Cell type' not in adata.obs.columns:
        print("column not found!")
    else:
        print("column exists!")
    adata_copy = adata.copy()
    scanpy.pl.umap(adata_copy[:50000], color=['Cell type', ], show=False) 
    
    
