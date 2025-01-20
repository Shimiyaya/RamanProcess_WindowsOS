import matplotlib

matplotlib.use("Qt5Agg")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import customtkinter as ctk
from tkinter import *
import pandas as pd
import numpy as np
from cosmic_window import CRRemoval
from baseline_removal2 import BaseCorrection
import time

# Base app class/window. All relevant variables are passed back here 
# two instances of other classes are created here - plot frame containing the spectra 
# and  questions frame containing the questions containing the option menus and submit buttons
# for cosmic ray correction and baseline correction
# these are actually corrected in breakout windows defined in separate modules 

class SpectraProcessGui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x600")
        self.title("Raman spectra processing")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue") 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # variables to define here and pass to and from next windows 
        self.X = None
        self.Y = None
        self.base_yn = None
        self.base_choice = ctk.StringVar(value="meow")
        self.cr_yn = None
        # line segment of cr ray removed
        self.cr_x = None
        self.cr_new_y = None


        self.cr_selected = None
        self.base_selected = None

        # plot frame class instance
        self.plot_frame = PlotFrame(self)
        self.plot_frame.grid(row=0, column=0, padx=(10,5), pady=(10, 0), sticky="nsew")

        # questions frame class instance
        self.questions_frame = QuestionsFrame(self, self.cr_selected, self.base_selected, self.base_choice, self.X, self.Y)
        self.questions_frame.grid(row=0, column=1, padx=(5,10), pady=(60, 60), sticky="nse")

    def clear_plot(self):
        self.plot_frame.clear_axes() 

    def update_plot_data(self, x,y, label_dt ):
         self.questions_frame.x = x
         self.questions_frame.y = y
         self.questions_frame.label_dt = label_dt
         self.plot_frame.update_plot(x,y, label_dt)  
         self.X = x
         self.Y = y
    def get_base_choice(self):
        return self.questions_frame.bc.fit_opt  
    
    def return_corrected_spectra(self):
        return self.Y
    
    def destroy_window(self):
        self.destroy()
        
    


class PlotFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.fig, self.ax = plt.subplots()
        plt.close(self.fig)
        self.canvas = FigureCanvasTkAgg(self.fig, master =self)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        #self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        #self.toolbar.update()
        self.canvas.draw()
        self.labels = []
        


    def clear_axes(self):
        self.ax.clear() 

    def reset_labels(self):
        self.labels = [] 

    def update_plot(self, x,y, label_dt):
        self.ax.scatter(x,y, label = label_dt) 
        self.ax.grid(True)
        self.labels.append(label_dt)
        self.ax.legend(self.labels)
        self.canvas.draw()           

class QuestionsFrame(ctk.CTkFrame):
    def __init__(self, parent, cr_selected, base_selected,base_choice, X, Y):
        super().__init__(parent) 
        self.x = X
        self.y=Y
        self.label_dt = None
        self.parent = parent

        # cosmic ray label, option menu and submit button
        self.cr_label = ctk.CTkLabel(self, text="Does this spectra contain cosmic rays?", fg_color="transparent")
        self.cr_label.pack(padx=10, pady=(10, 0), anchor="center")
        self.cr_optionmenu = ctk.CTkOptionMenu(self, values=["yes", "no"])
        self.cr_optionmenu.pack(padx=10, pady=(10, 0), anchor="center")
        #self.submit_buttonCR = ctk.CTkButton(self, text="Submit", command=self.button_eventCR) 
        #self.submit_buttonCR.pack(padx=10, pady=(20, 0), anchor="center")
        self.CR_opt = cr_selected


        # baseline correction label, button and option menu
        self.base_label = ctk.CTkLabel(self, text="Does this spectra require baseline correction?", fg_color="transparent")
        self.base_label.pack(padx=10, pady=(10, 0), anchor="center")       
        self.base_optionmenu = ctk.CTkOptionMenu(self, values=["yes", "no"])
        self.base_optionmenu.pack(padx=10, pady=(10, 10), anchor="center")
    
        self.submit_buttonCR = ctk.CTkButton(self, text="Submit", command=self.button_eventCR)
        self.submit_buttonCR.pack(padx=10, pady=(20, 0), anchor="center")
        self.baseline_opt =base_selected#=baseline_yn
        self.base_choice = base_choice

        # on submit button click, get the value of the option menu and open the breakout window
    def button_eventCR(self):
        self.CR_opt = self.cr_optionmenu.get()
        self.baseline_opt = self.base_optionmenu.get()
        if self.CR_opt == 'yes':
            self.open_CR_breakout_window(self.x, self.y) # open new CR window
        elif self.CR_opt == 'no':
            
            if  self.baseline_opt == 'yes':
                print(f"QF1 :{self.x}, {self.y}")
                self.open_baseline_breakout_window(self.x, self.y) # open new windo
            elif self.baseline_opt == 'no':
                self.parent.destroy()
    '''
    def button_eventBC(self):
        self.baseline_opt = self.base_optionmenu.get()
        if  self.baseline_opt == 'yes':
            print(f"QF1 :{self.x}, {self.y}")
            self.open_baseline_breakout_window(self.x, self.y) # open new windo
        elif self.baseline_opt == 'no':
            pass 
            '''
    def open_CR_breakout_window(self, X, Y ):
        print(f"self.baseline_opt: {self.baseline_opt}")
        cr = CRRemoval(self, X, Y, self.label_dt, self.baseline_opt)
        cr.grab_set()
    
    def open_baseline_breakout_window(self, X, Y):
        self.bc = BaseCorrection(self, X,Y, self.label_dt, self.base_choice)
        self.bc.grab_set() 
        
    def destroy_window(self):
        self.parent.destroy_window()
        #super().destroy()    


           



        
          
