import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import customtkinter as ctk
from tkinter import *
import pandas as pd
import numpy as np
import time
from baseline_removal2 import BaseCorrection

class CRRemoval(ctk.CTkToplevel):
    def __init__(self, parent, x, y, label, base_choice):
        super().__init__(parent)
        self.geometry("1000x600")
        self.title("Cosmic ray removal - select 2 points either side of the cosmic ray")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue") 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.X = x
        self.Y = y
        self.label = label
        self.base_choice = base_choice
        self.parent =  parent

        self.happy = ctk.StringVar()
        self.noise = ctk.StringVar(value = "0")

        self.frame = PlotFrame(self, self.X, self.Y, self.label)    
        self.frame.grid(row=0, column=0, padx=(10,5), pady=(10, 0), sticky="nsew")

        self.questions_frame =  ctk.CTkFrame(self)
        self.questions_frame.grid(row=0, column=1, padx=(5,10), pady=(20, 20), sticky="nse")

        self.noise_label =  ctk.CTkLabel(self.questions_frame, text="Noise addition to striaght line fit:") 
        self.noise_label.grid(row=0, column=0, padx=(5,10), pady=(100, 10), sticky="ne")

        self.noise_opt = ctk.CTkOptionMenu(self.questions_frame, values=["0", "5", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60", "65","70"], command = self.fit_noise, variable = self.noise)
        self.noise_opt.grid(row=1, column=0, padx=(5,10), pady=(10, 20), sticky="ne")

        self.happy_label = ctk.CTkLabel(self.questions_frame, text="Are you happy with the selection?") 
        self.happy_label.grid(row=2, column=0, padx=(5,10), pady=(20, 20), sticky="ne")

        self.happy_opt = ctk.CTkOptionMenu(self.questions_frame, values=["Yes", "No"], variable = self.happy)
        self.happy_opt.grid(row=3, column=0, padx=(5,10), pady=(20, 10), sticky="ne")

        self.happy_submit_button = ctk.CTkButton(self.questions_frame, text="Submit", command=self.happy_button_event)
        self.happy_submit_button.grid(row=4, column=0, padx=(5,10), pady=(20, 100), sticky="se")

        self.draw_plot_data(x, y)

        self.get_2_points()

    def draw_plot_data(self, x,y):# label_dt ):
         print(f"self.X, self.Y: {x, y}") 
         self.frame.draw_plot()#, label_dt)  

    def get_2_points(self):
        self.frame.select_2_points()
        x1 = self.frame.x1
        y1 = self.frame.y1

    def  happy_button_event(self):
        
        print(f"happy: {self.happy.get()}")
        if self.happy.get() == "Yes":
            # set y = to current selection 
            # grab the fitted line 
            # self.destroy()
            self.Y.iloc[int(self.frame.idx_list[0]):int(self.frame.idx_list[1])] = self.frame.segment_fit
            print(f"self.base_choice: {self.base_choice}")
            if self.base_choice == "yes":
                self.bc = BaseCorrection(self, self.X,self.Y, self.label, self.base_choice)
                self.bc.grab_set() 
                
                #self.destroy()
                #self.open_baseline_breakout_window(self.X, self.Y)
             
            else:
                self.destroy() 
                self.parent.destroy_window()

        if self.happy.get() == "No":
            self.clear_points()
            #self.destroy()

    def fit_noise(self, choice):
        self.frame.draw_noisy_line()      

    def clear_points(self):
        self.frame.remove_stars_from_graph()
        self.frame.reset_labels()  

    def open_baseline_breakout_window(self, X, Y):
        #self.destroy()
        self.bc = BaseCorrection(self, self.X,self.Y, self.label, "Check")
        self.bc.grab_set() 
        #self.destroy_window()

    def destroy_window(self):
        
        self.destroy()
        self.parent.destroy_window()
        #return super().destroy()             
       


class PlotFrame(ctk.CTkFrame):
    def __init__(self, parent, X, Y,label):
        super().__init__(parent)
        self.fig, self.ax = plt.subplots()
        plt.close(self.fig)
        self.canvas = FigureCanvasTkAgg(self.fig, master =self)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        #self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        #self.toolbar.update()
        self.canvas.draw()
        self.labels = []
        self.x = X
        self.y = Y

        self.x1 = ctk.DoubleVar(value=0.0)
        self.y1 = ctk.DoubleVar(value=0.0)
        self.x1_spectra = ctk.DoubleVar(value=0.0)
        self.y1_spectra = ctk.DoubleVar(value=0.0)
        self.idx1 = ctk.IntVar(value=0)

        self.x2 = ctk.DoubleVar(value=0.0)
        self.y2 = ctk.DoubleVar(value=0.0)
        self.x2_spectra = ctk.DoubleVar(value=0.0)
        self.y2_spectra = ctk.DoubleVar(value=0.0)
        self.idx2 = ctk.IntVar(value=0)

        self.n=ctk.IntVar(value=0)
        self.colors = ["blueviolet","deeppink"]
        self.label = label

        self.segment_fit = None
        self.line_fit = None
        self.parent = parent
        self.x_seg = None
        self.nfit = None

        #self.draw_plot()


    def clear_axes(self):
        self.ax.clear() 
        self.nfit = None

    def reset_labels(self):
        self.labels = [] 
        self.nfit = None

    def draw_plot(self):
        self.ax.scatter(self.x, self.y, label = self.label) 
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()  

    def draw_points(self):  
        if self.n.get() == 1:
            color = self.colors[0]
            self.ax.scatter(self.x1.get()  , self.y1.get(), label = f'clicked point {self.n.get()}', alpha = 0.5, c = color) 
        elif self.n.get() == 2:
            color = self.colors[1]
            self.ax.scatter(self.x2.get()  , self.y2.get(), label = f'clicked point {self.n.get()}', alpha = 0.5, c = color) 
        else:
            color = "black"    
        
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()  

    def draw_spectra_points(self):   
        if self.n.get() == 1:
            color = self.colors[0]
            self.ax.scatter(self.x1_spectra.get()  , self.y1_spectra.get(), label = f'spectra point {self.n.get()}',c=color) 
            self.ax.grid(True)
            self.ax.legend()
            self.canvas.draw() 
        elif self.n.get() == 2:
            color = self.colors[1]
            self.ax.scatter(self.x2_spectra.get()  , self.y2_spectra.get(), label = f'spectra point {self.n.get()}',c=color)
            self.ax.grid(True)
            self.ax.legend()
            self.canvas.draw() 
            self.draw_line() 
        else:
            color = "black"   
        
 

    def draw_line(self):

        self.idx_list = [self.idx1, self.idx2]
        self.idx_list = sorted(self.idx_list, reverse=False) # puts into descending order
        print(f"idx_list: {self.idx_list}")
        #x1_x2 = list([self.x1_spectra.get(), self.x2_spectra.get()]) # fix this: 
        x_segment = list(self.x["W"].iloc[int(self.idx_list[0]):int(self.idx_list[1])])
        
        #var = self.x["W"].iloc[(self.x["W"] - self.x1.get()).abs().argsort()[:2]] 
        print(f"x_segment: {x_segment}")
        #y1_y2 = list([self.y1_spectra.get(), self.y2_spectra.get()])
        y_segment = list(self.y.iloc[int(self.idx_list[0]):int(self.idx_list[1])])
        print(f"y_segment: {y_segment}")
        fit1 = np.poly1d(np.polyfit(np.array(x_segment), np.array(y_segment), deg = 1))
        #fit1 = np.poly1d(np.polyfit(x1_x2, y1_y2,1))
        print(f"fit1: {fit1}")


        # list of wavenumbers to fit to 
        #print(f"x_segment: {x_segment}")
        self.line_fit = np.polyval(fit1,x_segment)
        self.x_seg = x_segment
        print(f"line_fit: {self.line_fit}")


    def draw_noisy_line(self):
        if self.y2.get() == 0.0:
            pass 
        else:
        # end_point = idx_list[0]+len(line_fit)
        #noise_std = df["I"][x_fit2[0]:end_point].std() # gets the std of the sectio n next to what you're dealing with - not a greaat condition in case you're next to an actual feature 
            if self.nfit != None:       
                self.nfit.remove()
                #self.ax.self.nfit.pop()
                #self.ax.nfit.pop(-1)
            else:
                pass    
            noise_std = int(self.parent.noise.get())  
            noise = np.random.normal(0,noise_std, len(self.line_fit)) # change the noise condition to match that of a section of the actual spectra
            noisy_fit = self.line_fit+noise
            self.segment_fit = noisy_fit
            self.nfit = self.ax.scatter(self.x_seg  , noisy_fit, label = f'noisy fit: {noise_std}',c="maroon", alpha = 0.6) 
            self.ax.legend()
            self.canvas.draw() 


    def select_2_points(self):
        #self.title("Select 2 points either side of the cosmic ray")
        self.canvas.mpl_connect('button_press_event', self.record_ginput_events)
        #self.y1_check = self.canvas.mpl_connect('button_press_event', self.record_ginput_events)
        #self.draw_points()
        #return x1_check, x2_check   
        
    def record_ginput_events(self, event):
        while True:
            if self.n.get() ==0:
                # if self.x2 has already been set remove those points
                if self.x1.get() != 0.0:
                    self.remove_stars_from_graph
                else:
                    pass   
                self.x1.set(value =event.xdata)
                self.y1.set(value =event.ydata)
                self.n.set(value = (self.n.get()+1))
                self.draw_points()
                self.calc_spectra_points()
                
                break
            elif self.n.get() ==1: 
                # if self.x2 has already been set remove those points 
                if self.x2.get() != 0.0:
                    self.remove_stars_from_graph
                else:
                    pass 
                self.x2.set(value =event.xdata)
                self.y2.set(value =event.ydata)
                self.n.set(value = (self.n.get()+1)) 
                self.draw_points()
                self.calc_spectra_points()
                
                break

            elif self.n.get() > 1:
                self.n.set(value = 0)
                self.remove_stars_from_graph()


    def calc_spectra_points(self):
        #print(f"self.x type: {self.x.dtype()}")
        #self.x1_spectra.set(value=self.x.iloc[(self.x["W"] - self.x1.get()).abs()])#.argsort()[:2]]
        if self.n.get() == 1:
            var = self.x["W"].iloc[(self.x["W"] - self.x1.get()).abs().argsort()[:2]] # get the closest point in wavenumber to click point x value
            P1_x = var.values[0] # choose 1st value
            self.idx1 = var.index.to_list()[0]
            self.x1_spectra.set(value = P1_x)
            P1_y =  self.y.iloc[self.idx1]
            self.y1_spectra.set(value = P1_y)
            self.draw_spectra_points()
        elif self.n.get() == 2:
            var = self.x["W"].iloc[(self.x["W"] - self.x2.get()).abs().argsort()[:2]] # get the closest point in wavenumber to click point x value
            P2_x = var.values[0] # choose 1st value
            self.idx2 = var.index.to_list()[0]
            self.x2_spectra.set(value = P2_x)
            P2_y =  self.y.iloc[self.idx2]
            self.y2_spectra.set(value = P2_y)
            self.draw_spectra_points()    

        #print(f"spectra var : {P1_x} ,   {P1_y}")
        #print(f"spectra x : {var.index.tolist()}, {var.values}")
        



    '''
        x1 = df.W.iloc[(df['W']-x1_click).abs().argsort()[:2]]  
        x2 =  df.W.iloc[(df['W']-x2_click).abs().argsort()[:2]]  
        x =[x1.iloc[0],x2.iloc[0]] 
        x = sorted(x, reverse=True) # puts into descending order
        y1 = df.loc[df['W'] == x[0], 'I'].iloc[0]
        y2 = df.loc[df['W'] == x[1], 'I'].iloc[0]
        y = [y1,y2]
        # get the inices of x-co-ords
        x_fit1 = list(df["I"].loc[df['W'] == x[0]].index)
        x_fit2= list(df["I"].loc[df['W'] == x[1]].index)

        # create a straight line fit between these 2 points 
        fit1 = np.poly1d(np.polyfit(x, y,1))

        x_fit = list(df["W"][x_fit1[0]:x_fit2[0]]) # list of wavenumbers to fit to 
        line_fit = np.polyval(fit1,x_fit)
        
   
        end_point = x_fit2[0]+len(line_fit)
        #noise_std = df["I"][x_fit2[0]:end_point].std() # gets the std of the sectio n next to what you're dealing with - not a greaat condition in case you're next to an actual feature 
        noise_std = 25
        noise = np.random.normal(0,noise_std, len(line_fit)) # change the noise condition to match that of a section of the actual spectra
        noisy_fit = line_fit+noise
       '''










    def remove_stars_from_graph(self):
        self.labels = []
        self.ax.clear()
        self.nfit = None
        self.ax.scatter(self.x, self.y, label = self.label) 
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()  

