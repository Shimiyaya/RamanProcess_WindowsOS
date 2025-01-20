
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import customtkinter as ctk
from tkinter import *
import tkinter as tk
import pandas as pd
import numpy as np
import time
from BaselineRemoval import BaselineRemoval




class BaseCorrection(ctk.CTkToplevel):
    def __init__(self, parent, x, y, label, baseline_choice):
        super().__init__(parent)
        self.geometry("850x600")
        self.title("Baseline Correction")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue") 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.X = x
        self.Y = y 
        self.fit_opt = baseline_choice
        self.parent=parent
        
        self.label = label
        self.opt_menu_var = tk.StringVar()

        self.plot_frame = PlotFrame(self, self.X, self.Y, self.label)    
        self.plot_frame.grid(row=0, column=0, padx=(10,5), pady=(10, 10), sticky="nsw")

        self.questions_frame = ctk.CTkFrame(self)
        self.questions_frame.grid(row=0, column=1, padx=(5,10), pady=(20, 20), sticky="nse")

        self.best_fit_menu = ctk.CTkOptionMenu(self.questions_frame, values=["Zhang", "Modpoly", "iMod"],command = self.bring_y, variable = self.opt_menu_var)
        self.best_fit_menu.grid(row=0, column=0, padx=(5,10), pady=(200, 20), sticky="ne")

        self.bf_submit_button = ctk.CTkButton(self.questions_frame, text="Submit", command=self.bf_button_event)
        self.bf_submit_button.grid(row=1, column=0, padx=(5,10), pady=(20, 100), sticky="se")
        
        #self.opt_menu_var.trace_add("write", self.bring_y())
        #self.bring_y()

        self.draw_plot_data(x, y)
        

    def draw_plot_data(self, x,y):# label_dt ):
         #print(f"self.X, self.Y: {x, y}") 
         self.plot_frame.draw_plot()#, label_dt)  

    def bring_y(self, choice):
        print(f"check: {self.opt_menu_var.get()}")
        #fit_option = self.opt_menu_var.get()
       
        #
            #self.opt_menu_var = self.questions_frame.optmenu_var.get()
        self.plot_frame.bring_y_front(self.opt_menu_var.get()) 

    '''
    def change_y(self):
        print(f"{self.opt_menu_var.get()}")
        self.plot_frame.bring_y_front()  
            ''' 

    def bf_button_event(self):
        self.fit_opt = self.opt_menu_var.get()
        if self.fit_opt == "Zhang":
            self.Y = self.plot_frame.corrected_y1
            
            
        elif self.fit_opt == "Modpoly":  
            self.Y = self.plot_frame.corrected_y2

        elif self.fit_opt == "iMod": 
            self.Y = self.plot_frame.corrected_y3

        self.destroy_window()

    def destroy_window(self):
        self.parent.destroy_window()
        #super().destroy()    
        
        


class PlotFrame(ctk.CTkFrame):
    def __init__(self, parent, X, Y, label):
        super().__init__(parent)
        self.fig, self.ax = plt.subplots()
        plt.close(self.fig)
        self.canvas = FigureCanvasTkAgg(self.fig, master =self)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        #self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        #self.toolbar.update()
        self.canvas.draw()
        self.labels = label
        self.x = X
        self.y = Y
        self.base_color = "dimgray"
        baseObj = BaselineRemoval(self.y)

        self.corrected_y1 = baseObj.ZhangFit() 
        self.corrected_y1_label = "Zhang"
        self.y1_color = "palevioletred"

        self.corrected_y2 = baseObj.ModPoly(2)
        self.corrected_y2_label = "Modpoly"
        self.y2_color = "cornflowerblue"

        self.corrected_y3 = baseObj.IModPoly(2)   
        self.corrected_y3_label = "iMod"
        self.y3_color = "darkorange"

        self.optmenu_var = ctk.StringVar()
        self.base1 = object
        self.base2= object
        self.base3 = object

        #self.draw_plot()


    def clear_axes(self):
        self.ax.clear() 

    def reset_labels(self):
        self.labels = [] 

    def draw_plot(self):#, label_dt):
        #print(f"self.x, self.y: {self.x, self.y}")
        #baseObj = BaselineRemoval(self.y)
        self.ax.scatter(self.x, self.y, label = self.labels, c=self.base_color ) 
        #self.corrected_y1 = baseObj.ZhangFit() 
        self.base1 = self.ax.scatter(self.x, self.corrected_y1, label = self.corrected_y1_label, c = self.y1_color) 

        #self.corrected_y2 = baseObj.ModPoly(2)
        self.base2 = self.ax.scatter(self.x, self.corrected_y2, label =self.corrected_y2_label, c = self.y2_color)

        #self.corrected_y3 = baseObj.IModPoly(2)
        self.base3 = self.ax.scatter(self.x, self.corrected_y3, label =self.corrected_y3_label, c = self.y3_color)

        self.ax.grid(True)
        #self.labels.append(label_dt)
        self.ax.legend()
        self.canvas.draw() 

    def bring_y_front(self, fit_option):

        self.clear_axes()

        if fit_option == "Zhang":
            self.ax.scatter(self.x, self.corrected_y2, label = self.corrected_y2_label, alpha= 0.1,c = self.y2_color)
            self.ax.scatter(self.x, self.corrected_y3, label = self.corrected_y3_label, alpha= 0.1,c = self.y3_color)
            self.ax.scatter(self.x, self.y, label = self.labels, c=self.base_color) 
            self.ax.scatter(self.x, self.corrected_y1, label = self.corrected_y1_label, c = self.y1_color)
            
        elif fit_option == "Modpoly":  
            self.ax.scatter(self.x, self.corrected_y1, label = self.corrected_y1_label, alpha= 0.1, c = self.y1_color)
            self.ax.scatter(self.x, self.corrected_y3, label = self.corrected_y3_label, alpha= 0.1,c = self.y3_color) 
            self.ax.scatter(self.x, self.y, label = self.labels, c=self.base_color)
            self.ax.scatter(self.x, self.corrected_y2, label = self.corrected_y2_label,c = self.y2_color)

        elif fit_option == "iMod": 
            self.ax.scatter(self.x, self.corrected_y2, label = self.corrected_y2_label, alpha= 0.1,c = self.y2_color) 
            self.ax.scatter(self.x, self.corrected_y1, label = self.corrected_y1_label, alpha= 0.1, c = self.y1_color)
            self.ax.scatter(self.x, self.y, label = self.labels, c=self.base_color)  
            self.ax.scatter(self.x, self.corrected_y3, label = self.corrected_y3_label,c = self.y3_color)

        self.ax.grid(True)
        self.ax.legend()   
        self.canvas.draw()             




  

