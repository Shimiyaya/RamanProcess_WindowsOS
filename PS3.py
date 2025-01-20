import matplotlib

matplotlib.use("Qt5Agg")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import customtkinter as ctk
from tkinter import *
import tkinter as tk
#from SpectraGUI import *
#import SpectraGUI as sg
import pandas as pd
from GUI4 import SpectraProcessGui

def process_spectras(df, df_info):
    #spectra = SpectraProcessGui()
    for col in df:
        spectra = SpectraProcessGui()
        #cr_result = spectra.cr_selected.get() 
        spectra.clear_plot()
        spectra.update_plot_data(pd.DataFrame(df.index), df[col], col)
        print(f"check it1 : {spectra.get_base_choice}")
        spectra.mainloop()

        #print(f"check it : {spectra.get_base_choice()}")
        check = spectra.return_corrected_spectra()

        #plt.plot(df.index, check, '--.')
        #plt.show()


        #  print(f"in  process? {spectra.baseline_removal2.Y.get()}")
        # make sure they have recieved both corrections if required
        # get df after basline correction
        #spectra.get_baseline_df()
        # get df after cosmic ray removal
        #spectra.get_cr_df()
        # updat the main df
        df[col] = check 
        #print(f"{df[col]}")
        #plt.plot(df.index, df[col], '--.', label = col)
        #plt.legend()
        #plt.show()

    return df, df_info
