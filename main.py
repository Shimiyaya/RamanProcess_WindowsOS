#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 10:04:09 2024

@author: laurajodea
"""
import matplotlib

matplotlib.use("Qt5Agg")
from pathlib import Path
import pandas as pd
from config import FILE_PATHS
from ProcessRawRaman import get_files, build_dfs, process_df_other, add_to_final_df, save_df_to_csv
from ExcelBuilder import build_excel
from PS3 import process_spectras
import matplotlib.pyplot as plt

def main():
    # file path steps
    
    fp = Path(FILE_PATHS['READ_RAMAN'])
    fp_out = FILE_PATHS['SAVE_DFS']
    fp_out_excel = FILE_PATHS['SAVE_EXCEL']
    Path(fp_out).mkdir(parents=True, exist_ok=True)
    Path(fp_out_excel).mkdir(parents=True, exist_ok=True)
    csv_633 = 'spectra633.csv'
    csv_785 = 'spectra785.csv'
    csv_info = 'spectra_info.csv'
    folders=[1] # range of folders - this is the end of your folder name change it as you wish
    
    make_dfs = (input("Do you need to make the dataframe .csv files (y/n)? ")).lower().lstrip("").rstrip("")
    
    # %% dataframe builder
    if make_dfs =="y":
        combine_dfs = (input('Do you want to add new dataframes to existing ones (y/n)? ')).lower().lstrip("").rstrip("")
        if combine_dfs == 'y':
            df633 = pd.read_csv(Path(fp_out, csv_633))
            df633.set_index('W', inplace=True)
            df785 = pd.read_csv(Path(fp_out, csv_785))
            df785.set_index('W', inplace=True)
            df_info_fin = pd.read_csv(Path(fp_out, csv_info))
            for col in df_info_fin:
                if col.startswith("Unnamed"):
                    df_info_fin.drop(columns=[col], inplace = True)
                else:
                    pass
                    
        else:
            df633 = pd.DataFrame()
            df785= pd.DataFrame()
            df_info_fin =pd.DataFrame()
           
        # read in all files and scrape info
        for folder in folders:
            fp_dict, docs2, list_docs = get_files(fp,folder)
            df_633, df_785, df_wn_other_633,df_wn_other_785, df_info  = build_dfs(fp_dict, docs2, list_docs)
            # add a condition to ask if its something the user wants to do 
            #TODO: cosmic ray removal here 
            
            df_633,df_info = process_spectras(df_633, df_info)
            df_785, df_info = process_spectras(df_785, df_info)
            #TODO: fix this so that it only sends in 1 wavelength-index pair at a time
            if not df_wn_other_633.empty:
                col_names = df_wn_other_633.columns
                num_wn = [x.startswith("W") for x in col_names]
                for wn in range(sum(num_wn)):
                    df_test =pd.DataFrame( df_wn_other_633.iloc[:,((wn*2) +1)])
                    df_test.set_index(df_wn_other_633.iloc[:,(wn*2)], inplace=True)
                    df_test.index.name = "W"
                    df_test, df_info = process_spectras(df_test, df_info)
                    df_wn_other_633.iloc[:,((wn*2) +1)] = df_test.iloc[:,0]
            else:
                pass
            if not df_wn_other_785.empty:
                col_names = df_wn_other_785.columns
                num_wn = [x.startswith("W") for x in col_names]
                for wn in range(sum(num_wn)):
                    df_test =pd.DataFrame( df_wn_other_785.iloc[:,((wn*2) +1)])
                    df_test.set_index(df_wn_other_785.iloc[:,(wn*2)], inplace=True)
                    df_test.index.name = "W"
                    df_test, df_info = process_spectras(df_test, df_info)
                    df_wn_other_785.iloc[:,((wn*2) +1)] = df_test.iloc[:,0]
                #df_wn_other_785, df_info = process_spectras(df_wn_other_785, df_info)
            else:
                pass
            
            
            if not df_wn_other_633.empty:
                df_633 = process_df_other(df_633, df_wn_other_633, df_info )
            else:
                pass
            if not df_wn_other_785.empty:
                df_785 = process_df_other(df_785, df_wn_other_785, df_info)
            else:
                pass
            last_num = df_info_fin.shape[0]
            df633, df_info = add_to_final_df(df633, df_633, df_info, last_num)
            #df_info_fin = update_info_names(df_info, df_info_fin, id_dict)
            df785, df_info = add_to_final_df(df785, df_785, df_info, last_num)
            #df_info_fin = update_info_names(df_info, df_info_fin, id_dict)
            df_info_fin = pd.concat([df_info_fin, df_info], axis=0)
            # %% save files as csv     
            save_df_to_csv(df633, fp_out, csv_633) 
            save_df_to_csv(df785, fp_out, csv_785) 
            save_df_to_csv(df_info_fin, fp_out, csv_info) 
    else:
        pass
    
    # %% export to excel file
    make_xlsx = (input("Do you need to make the excel file (y/n)? ")).lower().lstrip("").rstrip("")
    if make_xlsx == 'y':
        fn_excel = "Raman.xlsx"
        ref_frac = 0.8
        build_excel(fp_out, csv_633, csv_785, csv_info, fp_out_excel, fn_excel, ref_frac)
    else:
        pass
    

    #return df633, df785, df_info_fin
    





if __name__ == "__main__":
    main()
    #df633, df785, df_info = main()