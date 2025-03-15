import shiny 
import scanpy as sc 
import zipfile 
import matplotlib 
import matplotlib.pyplot 
import os 
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
# plt.style.use('dark_background')

import seaborn as sns

from sklearn.decomposition import PCA
#file upload button that accepts h5ad formatted files

from shiny import App, Inputs, Outputs, Session, reactive, render,ui
from zipfile import ZipFile

from shiny.types import FileInfo
import umapcodes #codes needed for umap visualization importet as module

app_ui = ui.page_fluid(
    ui.input_file("file1", "Choose zip File", accept=[".zip"], multiple=False),
    ui.output_table("summary"),
    ui.h1("Single-Cell Data UMAPViewer in Shiny for Python"),
    ui.output_plot("umap_plot")
)


def server(input: Inputs, output: Outputs, session: Session):
    @output
    @render.plot
    @reactive.event(input.file1) 
    def umap_plot():
        file = input.file1()  
        if file is not None:  # Dosya yüklendiyse
            if isinstance(file, list):  # Eğer file bir liste ise
                file_path = file[0]['datapath']  # İlk dosyanın yolunu al
            else:
                file_path = file[0]["data_path"]
            
            timestamp = int(time.time())  # Get current time in seconds
            extracted_folder = f"extracted_data_{timestamp}"
            unzip_file(file_path, extracted_folder)
            extracted_files = os.listdir(extracted_folder)
            print(f"Files in extracted folder: {extracted_files}")
            h5ad_files = [f for f in os.listdir(extracted_folder) if f.endswith('.h5ad')]
            
            if not h5ad_files:
                print("No .h5ad file found in the extracted folder")
                return
            
            
        adata_file = h5ad_files[0]
        adata = sc.read(os.path.join(extracted_folder, adata_file))
        adata = filter(adata) 
        cluster(adata)
        return plot(adata)


            
App(app_ui, server) 
app = App(app_ui,server)
