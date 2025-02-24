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
    ui.input_file("f", "Choose h5ad File", accept=[".h5ad"], multiple=False),
    ui.input_checkbox_group(
        "stats",
        "Summary Stats",
        choices=["Row Count", "Column Count", "Column Names"],
        selected=["Row Count", "Column Count", "Column Names"],
    ),
    ui.output_table("summary"),
)

#data processing component
def server(input: Inputs, output: Outputs, session: Session):
    @output     
    @reactive.calc #repeats itself when user adds new file
    def parsed_file():
        file: list[FileInfo] | None = input.f()
        if file is None:
            return pd.DataFrame()
        return pd.read_h5ad(  # pyright: ignore[reportUnknownMemberType]
            file[0]["uploadedfile"]  
        )
    ploting_data = umapcodes
@render.table #displays the output of summary() as table
def summary():#processes the data gathered from parsed file
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
