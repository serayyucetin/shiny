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
#user interface 
app_ui = ui.page_fluid(
    ui.input_file("file1", "Choose zip File", accept=[".zip"], multiple=False),
    ui.input_checkbox_group(
        "stats",
        "Summary Stats",
        choices=["Row Count", "Column Count", "Column Names"],
        selected=["Row Count", "Column Count", "Column Names"],
    ),
    ui.output_table("summary"),
    ui.h1("Single-Cell Data UMAPViewer in Shiny for Python"),
    ui.output_image("final_plot")
)


def server(input: Inputs, output: Outputs, session: Session):
    @output
    def unzip_file(zip_path, extract_to):
        with zipfile.ZipFile(zip_path,'r') as zip_ref:
            zip_ref.extractall(extract_to)    
    @output
    @reactive.calc
    def parsed_file():
        file: list[FileInfo] | None = input.file1()
        try:
            if file is None:
                return pd.DataFrame()
                return pd.read_h5ad( 
                      file[0]["datapath"] )
        except:
            return f"file uploaded"
    @output
    @render.table
    def summary():
        df = parsed_file()

        if df.empty:
            return pd.DataFrame()
