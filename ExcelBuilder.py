#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 11:06:00 2024

@author: laurajodea
"""

from pathlib import Path
import pandas as pd
import xlsxwriter
from string import ascii_uppercase
from itertools import product

def build_excel(fp_csv, csv_633, csv_785, csv_info, fp_out_excel,xlsx_name, ref_fac):
    # read in dataframes from csv files   
    df_633  = pd.read_csv(Path(fp_csv, csv_633))
    df_785  = pd.read_csv(Path(fp_csv, csv_785))
    df_info = pd.read_csv(Path(fp_csv, csv_info))

        
    # determine no sheets needed, so. samples, and no. sites per sample
    num_sheets = (df_info.CNT_reaction.nunique()) * 2  # the number of sheets in your work book is number of CNT reactionsx2 for both wavelengths
    sheet_name = df_info.CNT_reaction.unique()
    num_samples = df_info.groupby("CNT_reaction").Sample_no.unique()
    num_sites = df_info.groupby(["CNT_reaction", "Sample_no"]).sample_site_no.nunique()
    sites_list= df_info.groupby(["CNT_reaction", "Sample_no"]).sample_site_no.unique()
    OG_633 = []
    Norm1_633 = []
    OG_785 = []
    Norm1_785=[]  
    
    pool = list(map(''.join, product(['']+list(ascii_uppercase), list(ascii_uppercase))))
    dict_pool = dict(enumerate(pool))
    
    # %% the style section - change cell formating here
    header_style = {
            "bold": True,
            "text_wrap": True,
            "bg_color" : '#D0D5D5' ,
            "valign": "middle",
            "align": "middle",
            #"fg_color": "#7F8D90",
            "border": 0,
            "bottom": 1
        }
    
    index_style={
            "bold": True,
            "border": 0,
            "right" :1,
            "left" :1,
            "bg_color" : '#E9EAEA' 
             }
    
    #  %% Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(Path(fp_out_excel,xlsx_name), engine="xlsxwriter")
    workbook=writer.book # opens the workbook to write (from scratch)
    w1 = '633nm'
    w2 = '785nm'
    
    for n, CNT_R in enumerate(sheet_name):
        df_OG_633 = pd.DataFrame()
        df_OG_785 = pd.DataFrame()
        df_Norm1_633 = pd.DataFrame()
        df_Norm1_633_WN = pd.DataFrame()
        df_Norm1_785 = pd.DataFrame()
        df_Norm1_785_WN = pd.DataFrame()
        df_excel =  pd.DataFrame()
        no_samples = num_samples.tolist()
        samps = no_samples[n] 
        OG_633 = []
        Norm1_633 = []
        OG_785 = []
        Norm1_785=[]
        for samp in samps:
            
            # 633 first
            filtered_633 = df_info[(df_info["CNT_reaction"]==CNT_R) & (df_info["Sample_no"]==samp) & (df_info["wavelength"]==w1)]
            filtered_633 .sort_values(by='sample_site_no', ascending=True, inplace=True)
            for index, site in filtered_633.iterrows():
                ID = site["item_ID"]
                title =  "TT_" + "{:03d}".format(CNT_R)+ "_"+str(samp)+"_" + str(site["sample_site_no"]) 
                OG_633.append({
                    title: df_633[ID].values.tolist()
                     })
                # normalised 633 - 1
                norm1 = [(x/(max(df_633[ID].values.tolist())))*100 for x in df_633[ID].values.tolist()]
                Norm1_633.append({
                    title+"_N": norm1
                    })
            # build 785    
            filtered_785 = df_info[(df_info["CNT_reaction"]==CNT_R) & (df_info["Sample_no"]==samp) & (df_info["wavelength"]==w2)]
            filtered_785 .sort_values(by='sample_site_no', ascending=True, inplace=True)
            for index, site in filtered_785.iterrows():
                ID = site["item_ID"]
                title =  "TT_" + "{:03d}".format(CNT_R) + "_"+str(samp)+"_" + str(site["sample_site_no"])
                OG_785.append({
                    title: df_785[ID].values.tolist()
                    })
                # normalized 785 -1 
                norm1 = [(x/(max(df_785[ID].values.tolist())))*100 for x in df_785[ID].values.tolist()]
                Norm1_785.append({
                    title+"_N": norm1
                    })
                
        df_OG_633 = pd.concat([pd.DataFrame(data) for data in OG_633], axis=1)
        df_Norm1_633 = pd.concat([pd.DataFrame(data) for data in Norm1_633], axis=1) 
        df_OG_633.index = df_633['W']
        df_OG_633 = df_OG_633.reset_index()
        df_Norm1_633.index = df_633['W']
        df_Norm1_633 = df_Norm1_633.reset_index()
        df_Norm1_633_WN = pd.concat([df_Norm1_633,df_633['W']], axis = 1, ignore_index = False )
        df_excel = pd.concat([df_OG_633, df_Norm1_633, df_Norm1_633],axis = 1,ignore_index=False)  
        
        # 633 sheet
        sheet_name_w1 ='TT-'+"{:03d}".format(CNT_R)+'-' +w1
        worksheet=workbook.add_worksheet(sheet_name_w1) 
        writer.sheets[sheet_name_w1] = worksheet
        df_excel.to_excel(writer, sheet_name = sheet_name_w1, index=True, header = True)
        
        # ref table 
        ref_frac = 0.8
        df_shape = df_OG_633.shape
        sc = int(((df_excel.shape)[1] *1.1) + 1) 
        sc_letter = dict_pool[sc]
   
        ref_633 = list((range(df_shape[1])))
        ref_633 = [x*100 for x in ref_633 ]
        ref_633.append(ref_frac)
        lc = sc+ len(ref_633)
        
        # normalised 2 
        df_excel.to_excel(writer, sheet_name = sheet_name_w1, index=True, header = True)
        df_ref_633 = pd.DataFrame([ref_633], columns = [f'Ref_value{i+1} ' for i in range(len(ref_633))])
        df_ref_633.to_excel(writer, sheet_name = sheet_name_w1, startrow =0 , startcol= sc, header=False, index=False)

        # add a loop for this, add cell referencing and add one more wavelength col
        for col_num in range(df_OG_633.shape[1]):
            col_letter = dict_pool[((df_Norm1_633.shape[1])*2 +1+col_num)]
            cell_str = col_letter+'2:'+col_letter+str((df_Norm1_633.shape[0])+1)
            col_ref = dict_pool[df_OG_633.shape[1]+col_num+1]
            col_str = '('+col_ref+'2:'+col_ref+str((df_Norm1_633.shape[0])+1)+')' # (M2:M1869)
            ref_multiplier1 = dict_pool[(sc+col_num)]
            ref_multiplier2 = dict_pool[(lc-1)] 
            cell_formula = '{='+col_str +'+' + ref_multiplier1 +'1*' + ref_multiplier2 + '1}'
            worksheet.write_array_formula(cell_str, cell_formula) 

        # add cell formatting 
        header_format = workbook.add_format(header_style)
        index_format = workbook.add_format(index_style)
        for col_num, value in enumerate(df_excel.columns.values):
           if value == "W":
               for idx1, idx2 in enumerate(df_excel.iterrows()): 
                   worksheet.write(idx1+1, col_num + 1, df_633.W.iloc[idx2[0]], index_format)
           worksheet.write(0, col_num + 1, value, header_format)
        worksheet.set_column(0, df_excel.shape[1], 20)
        
        chart = workbook.add_chart({"type": "line"})
        # Configure the series of the chart from the dataframe data.
        for i in range(df_OG_633.shape[1]-1):
            col = (df_excel.shape[1] -(df_OG_633.shape[1])) +2+ i 
            x_col = (df_excel.shape[1] -(df_OG_633.shape[1]))+1
            max_row = df_excel.shape[0]+1
            chart.add_series(
                {
                    "name": [sheet_name_w1, 0, col],
                    "categories": [ sheet_name_w1, 1, x_col, max_row, x_col],
                    "values": [sheet_name_w1, 1, col, max_row, col],
                    }
                )
        chart.set_x_axis({"name": "Wave no. cm^{-1}"})
        chart.set_y_axis({"name": "Normalized Intensity", "major_gridlines": {"visible": True}})  
        worksheet.insert_chart(sc_letter+str(4), chart)

        
        # %% 785 section 
        df_OG_785 = pd.concat([pd.DataFrame(data) for data in OG_785], axis=1)
         #df_OG_633.index = df_633["Wave_num"]  
        df_Norm1_785 = pd.concat([pd.DataFrame(data) for data in Norm1_785], axis=1) 
        df_OG_785.index = df_785["W"]
        df_OG_785 = df_OG_785.reset_index()
        df_Norm1_785.index = df_785["W"] 
        df_Norm1_785 = df_Norm1_785.reset_index()
        df_excelb = pd.concat([df_OG_785, df_Norm1_785, df_Norm1_785],axis = 1,ignore_index=False)
        

        # 785 sheet
        sheet_name_w2='TT-'+"{:03d}".format(CNT_R)+'-' +w2
        worksheet_w2=workbook.add_worksheet(sheet_name_w2) 
        writer.sheets[sheet_name_w2] = worksheet_w2
        
        # ref table 785
        df_shape = df_OG_785.shape
        sc = int(((df_excelb.shape)[1] *1.1) + 1) 
        sc_letter = dict_pool[sc]   
        ref_785 = list(range(df_shape[1]))
        ref_785 = [x*100 for x in ref_785 ]
        ref_785.append(ref_frac)
        lc = sc+ len(ref_785)
          
        # normalized 2
        df_excelb.to_excel(writer, sheet_name=sheet_name_w2, index=True,  header = True)
        df_ref_785 = pd.DataFrame([ref_785], columns = [f'Ref_value{i+1} ' for i in range(len(ref_785))])
        df_ref_785.to_excel(writer, sheet_name = sheet_name_w2, startrow =0 , startcol= sc, header=False, index=False)
        
        
        # add a loop for this, add cell referencing and add one more wavelength col
        for col_num in range(df_OG_785.shape[1]):
            col_letter = dict_pool[((df_Norm1_785.shape[1])*2 +1+col_num)]
            cell_str = col_letter+'2:'+col_letter+str((df_Norm1_785.shape[0])+1)
            col_ref = dict_pool[df_OG_785.shape[1]+col_num+1]
            col_str = '('+col_ref+'2:'+col_ref+str((df_Norm1_785.shape[0])+1)+')' # (M2:M1869)
            ref_multiplier1 = dict_pool[(sc+col_num)]
            ref_multiplier2 = dict_pool[(lc-1)] 
            cell_formula = '{='+col_str +'+(' + ref_multiplier1 +'1*' + ref_multiplier2 + '1)}'
            worksheet_w2.write_array_formula(cell_str, cell_formula) 
        
         # add cell formatting 
        header_format = workbook.add_format(header_style)
        index_format = workbook.add_format(index_style)
        for col_num, value in enumerate(df_excelb.columns.values):
            if value == "W":
                for idx1, idx2 in enumerate(df_excelb.iterrows()): 
                    worksheet_w2.write(idx1+1, col_num + 1, df_785.W.iloc[idx2[0]], index_format)
            worksheet_w2.write(0, col_num + 1, value, header_format)
        worksheet_w2.set_column(0, df_excelb.shape[1], 20)
        
          
        chart = workbook.add_chart({"type": "line"})
        # Configure the series of the chart from the dataframe data.
        for i in range(df_OG_785.shape[1]-1):
            col = (df_excelb.shape[1] -(df_OG_785.shape[1])) +2+ i 
            x_col = (df_excelb.shape[1] -(df_OG_785.shape[1]))+1
            max_row = df_excelb.shape[0]+1
            chart.add_series(
                {
                    "name": [sheet_name_w2, 0, col],
                    "categories": [ sheet_name_w2, 1, x_col, max_row, x_col],
                    "values": [sheet_name_w2, 1, col, max_row, col],
                    }
                )
        chart.set_x_axis({"name": "Wave no. cm^{-1}"})
        chart.set_y_axis({"name": "Normalized Intensity", "major_gridlines": {"visible": True}})  
        worksheet_w2.insert_chart(sc_letter+str(4), chart)
        

    writer.close()  
    
