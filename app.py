import shiny 
import scanpy as sc 
import zipfile 
import matplotlib 
import matplotlib.pyplot 
import os 
import scanpy 
#umap için gerekliler
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
#file upload button that accepts h5ad formatted files

from shiny import App, Inputs, Outputs, Session, reactive, render,ui
from zipfile import ZipFile

from shiny.types import FileInfo


#file upload butonunun kodu 
app_ui = ui.page_fluid(
    ui.input_file("f", "Choose h5ad File", accept=[".h5ad"], multiple=False),
    ui.input_checkbox_group(
        "stats",
        "Summary Stats",
        choices=["Row Count", "Column Count", "Column Names"],
        selected=["Row Count", "Column Count", "Column Names"],
    ),
    ui.output_table("summary"),
)


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.calc
    def parsed_file():
        file: list[FileInfo] | None = input.f()
        if file is None:
            return pd.DataFrame()
        return pd.read_h5ad(  # pyright: ignore[reportUnknownMemberType]
            file[0]["datapath"]
        )
@render.table
def summary():
        df = parsed_file()

        if df.empty:
            return pd.DataFrame()

        # Get the row count, column count, and column names of the DataFrame
        row_count = df.shape[0]
        column_count = df.shape[1]
        names = df.columns.tolist()
        column_names = ", ".join(str(name) for name in names)

        # Create a new DataFrame to display the information
        info_df = pd.DataFrame(
            {
                "Row Count": [row_count],
                "Column Count": [column_count],
                "Column Names": [column_names],
            }
        )

        # input.stats() is a list of strings; subset the columns based on the selected
        # checkboxes
        return info_df.loc[:, input.stats()]


app = App(app_ui, server)





app_ui = ui.page_fluid(
    ui.row(
        ui.input_selectize('entry', 'User input', choices=[i for i in range(10)]),
        ui.input_action_button('submit', 'Submit'),
        id='selection_ui'
        )
    )

def server(input, output, session):
    
    session_nb_plot = reactive.Value(0)
    
    @reactive.Effect
    @reactive.event(input.submit)
    def _add():
        
        entry = input.entry()
        
        ui.insert_ui(
            make_plot(entry),
            selector='#selection_ui',
            where='afterEnd'
            )

        
    def make_plot(entry):
        
        @output
        @render.plot
        def plot_logic():
            fig = plt.figure()
            plt.plot(entry,'rD')
            return fig
        
        nb_plot = session_nb_plot.get()
        
        plot = ui.panel_well(
            ui.input_action_button('remove_'+str(nb_plot), 'Remove'),
            ui.output_plot('plot_logic'), # comment this line if you want to see how it works without the plot part
            id="to_remove_"+str(nb_plot)
            )
        
        session_nb_plot.set(nb_plot+1)
        
        return plot
   

    @reactive.Effect
    def _remove():
        
        nb_plot = session_nb_plot.get()

        if nb_plot != 0:
            for i in range(nb_plot):
                if input['remove_'+str(i)]():
                    ui.remove_ui('#to_remove_'+str(i))
            
        
app = App(app_ui, server)

def file_path = ''
    if 1:  
        t0 = time.time()
        adata = scanpy.read(file_path)
        print('%.1f'%(-t0+time.time()), ' seconds passed' )
        print(type(adata.X))
        adata
        from shiny import App, render, ui, reactive
import matplotlib.pyplot as plt

#asıl kod ama app design kısmı yok.Çalışmıyor.

scanpy.pl.violin(adata, ['n_genes_by_counts', 'total_counts'],jitter=0.4, multi_panel=True)
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
scanpy.pl.highly_variable_genes(adata)
adata = adata[:, adata.var.highly_variable]

scanpy.pp.scale(adata, max_value=10) # subtract the mean expression value and divide by the standard deviation
adata
scanpy.pp.neighbors(adata, n_neighbors=10, n_pcs=40)
scanpy.tl.umap(adata)
scanpy.pl.umap(adata, color=['n_genes_by_counts', 'total_counts'])  
scanpy.pl.umap(adata, color=['Cell type'])
scanpy.pl.umap(adata, color='Cell type', groups=['Myeloid'])
