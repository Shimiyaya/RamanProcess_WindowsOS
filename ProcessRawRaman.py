#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 10:16:53 2024

@author: laurajodea
"""

import os
import re
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from pathlib import Path

#from config import LIST_DOCS, LIST_TXTS, LIST_WDFS, LIST_WDFS_MOD, TXT_MATRIX, ITEM_ID, CNT_REACTION,SAMPLE_NO, WAVELENGTH ,AQ_TIME,LASER_POWER, ACCUM_NO ,SAMPLE_SITE_NO ,BASELINE_REQ
#from config import COSMIC_RAYS,LABELS ,DOCS2,   FP_DICT ,NN,DF_633,DF_633_B ,DF_785 ,DF_785_B ,DF_INFO,NUM ,NUM_633,NUM_785, DF_WN_OTHER_633, DF_WN_OTHER_785

def get_files(fp,folder):
    LIST_DOCS = []
    LIST_TXTS = []
    LIST_WDFS = []
    LIST_WDFS_MOD = []
    TXT_MATRIX = []
    ITEM_ID = []
    CNT_REACTION = []
    SAMPLE_NO= []
    WAVELENGTH = []
    AQ_TIME = []
    LASER_POWER =[]
    ACCUM_NO = []
    SAMPLE_SITE_NO = []
    BASELINE_REQ = []
    COSMIC_RAYS = []
    LABELS = []
    DOCS2 = []   
    FP_DICT = {}
    #DF_CHECKLIST = pd.dataframe(columns = ['id', "cosmic_rays", "baseline", "label"])
    NN=0
    DF_633 = pd.DataFrame()
    DF_633_B = pd.DataFrame()
    DF_785 = pd.DataFrame()
    DF_785_B = pd.DataFrame()
    DF_INFO = pd.DataFrame()
    DF_WN_OTHER_633 = pd.DataFrame()
    DF_WN_OTHER_785 = pd.DataFrame()
    NUM = 0
    NUM_633 = 0
    NUM_785 = 0
    #for folder in folders:
        # gets full list of all files from folder in folders list
    # TODO: add system reader and change  \\ if windows and / if mac
    fn_extra = "TT-"+"{:03d}".format(folder)+"\\"   
    fp_full = Path(fp , fn_extra)
    docs_extra = os.listdir(fp_full)
    FP_DICT[fp_full] = docs_extra
    DOCS2.append(DOCS2)
    LIST_DOCS.append(docs_extra)
        
    return    FP_DICT,   DOCS2, LIST_DOCS

def build_dfs(FP_DICT, DOCS2, LIST_DOCS):
   
    LIST_TXTS = []
    LIST_WDFS = []
    LIST_WDFS_MOD = []
    TXT_MATRIX = []
    ITEM_ID = []
    CNT_REACTION = []
    SAMPLE_NO= []
    WAVELENGTH = []
    AQ_TIME = []
    LASER_POWER =[]
    ACCUM_NO = []
    SAMPLE_SITE_NO = []
    BASELINE_REQ = []
    COSMIC_RAYS = []
    LABELS = []
  
    #DF_CHECKLIST = pd.dataframe(columns = ['id', "cosmic_rays", "baseline", "label"])
    NN=0
    DF_633 = pd.DataFrame()
    DF_633_B = pd.DataFrame()
    DF_785 = pd.DataFrame()
    DF_785_B = pd.DataFrame()
    DF_INFO = pd.DataFrame()
    DF_WN_OTHER_633 = pd.DataFrame()
    DF_WN_OTHER_785 = pd.DataFrame()
    NUM = 0
    NUM_633 = 0
    NUM_785 = 0
    #global NUM, NUM_633,NUM_785 , DF_633, DF_785, DF_INFO , DF_WN_OTHER_633, DF_WN_OTHER_785 
    flat_list = [item for sublist in LIST_DOCS for item in sublist]        
    DOCS2 =  [item for sublist in DOCS2 for item in sublist] 
    
    fp_dict2 = {item: key for key , items in FP_DICT.items() for item in items}
    
    # %% mostly deconstructing the file name 
    for n, item in enumerate(flat_list):
        
        try :
             # %% finds the txt files in the listed docs
             if re.match(".*\.txt$" ,item):
                 NUM += 1
                 LIST_TXTS.append(item)
                 # read in from file
                 # TODO: change to make the index = wn 
                 txt_file = pd.read_csv(Path(fp_dict2[item],item),  sep = "\t",  encoding='unicode_escape')
                 c=txt_file.isnull().values.all(axis=0)
                 txt_file =txt_file[txt_file.columns[~c]]
                 txt_file = txt_file.rename(columns = {'#Wave': 'W', 'Unnamed: 1' : 'I'})
                 txt_file.set_index("W", inplace=True, drop=True)
    
             else:
                 pass
             
             #  gets info about the sample from the txt file name
             pattern = "^(?P<comp_name>(TT))(?:(-|__|_))(?P<CNT_R>\d{3})(?:(-|__|_))(?P<S_no>\d+)(?:(-|__|_))(?P<wave>\d{3}nm)(?:(-|__|_))(?P<Aq_t>\d+s)(?:(-|__|_))(?P<lp>\d+\.?\d?\d?\%*)(?:(-|__|_))(?P<ac_no>\d+)(?:(-|__|_))(?P<site_no>\d+)(?P<ext>\.(txt))$"
             match = re.match(pattern,item)    
             CNT_REACTION.append(match.groupdict()["CNT_R"])
             SAMPLE_NO.append(match.groupdict()["S_no"])
             WAVELENGTH.append(match.groupdict()["wave"])
             AQ_TIME.append(match.groupdict()["Aq_t"])
             LASER_POWER.append(match.groupdict()["lp"])
             ACCUM_NO.append(match.groupdict()["ac_no"])   
             SAMPLE_SITE_NO.append(match.groupdict()["site_no"])
             
             # creates new ID name for each sample thats easy to iterate over
             id_name = "TT-R-" + "{:03d}".format(NUM)
             ITEM_ID.append(id_name)
             
             if (match.groupdict()["wave"]) ==  "633nm":
                 NUM_633 += 1                    
                 if DF_633.empty: # initialises the first instance of the df for that wavelength
                    # TODO: change to DF_633 = tx_file dataframe, still rename the col               
                    txt_file.rename(columns = {'I': id_name}, inplace = True)
                    
                    DF_633 = txt_file
                    #DF_633.set_index('W', inplace=True)
                    #txt_file.iloc[0:0]
                 else:
                 # check wave_nums are the same condition
                 # TODO: change to check the index of DF_633 (adds a 2nd check to make sure they are the same wn)
                     if DF_633.index.equals(txt_file.index):
                         #TODO: determine whether join, merge or concat is the best to use here
                         txt_file.rename(columns = {'I': id_name}, inplace = True)
                         DF_633 = DF_633.join(txt_file, how='left')
                         #txt_file.iloc[0:0]
    
                     else:
                         print(f"Warning: file {item} placed in extra df due to wavenumber mismatch")
                         # TODO: make sure the df other can contain columns of different sizes 
                         txt_file.reset_index(inplace=True)
                         txt_file.rename(columns = { 'index':'W', 'I': id_name}, inplace = True)
                         DF_WN_OTHER_633 = pd.concat([DF_WN_OTHER_633, txt_file], axis = 1, join='outer', ignore_index=False )  # this join opt can concat columns of dif length and fill blanks with NaNs
                         #txt_file.iloc[0:0]
                         
             elif (match.groupdict()["wave"]) ==  "785nm":  
                 NUM_785 += 1 
                 if  DF_785.empty:
                     txt_file.rename(columns = {'I': id_name}, inplace = True)
                     DF_785 = txt_file
                     #DF_785.set_index('W', inplace=True)
                     #txt_file.iloc[0:0]
                 else:
                     # check wave_nums are the same condition
                     if DF_785.index.equals(txt_file.index):
                         txt_file.rename(columns = {'I': id_name}, inplace = True)
                         DF_785 = DF_785.join(txt_file, how='left')
                         #txt_file.iloc[0:0]
                     else:
                         print(f"Warning: file {item} placed in extra df due to wavenumber mismatch") 
                         txt_file.reset_index(inplace=True)
                         txt_file.rename(columns = { 'W':'W'+id_name, 'I': id_name}, inplace = True)
                         DF_WN_OTHER_785 = pd.concat([DF_WN_OTHER_785, txt_file], axis = 1, join='outer', ignore_index=False )  # this join opt can concat columns of dif length and fill blanks with NaNs
                         #txt_file.iloc[0:0]              
        except AttributeError:
             print(item)
        # Build the df_info supporting info df  
     # clears txt file for next run  
    if DF_INFO.empty:
        DF_INFO = pd.DataFrame(
            {'item_ID' :ITEM_ID,
             'txt_fn': LIST_TXTS,
                'CNT_reaction': CNT_REACTION,
         'Sample_no': SAMPLE_NO,
         'wavelength': WAVELENGTH,
         'aq_time': AQ_TIME,
         'laser_power' :LASER_POWER,
         'accum_no': ACCUM_NO,
         'sample_site_no': SAMPLE_SITE_NO,
         'sample_site_no':  SAMPLE_SITE_NO     
         })
    else:
        DF_INFO2 = pd.DataFrame(
            {'item_ID' :ITEM_ID,
             'txt_fn': LIST_TXTS,
                'CNT_reaction': CNT_REACTION,
         'Sample_no': SAMPLE_NO,
         'wavelength': WAVELENGTH,
         'aq_time': AQ_TIME,
         'laser_power' :LASER_POWER,
         'accum_no': ACCUM_NO,
         'sample_site_no': SAMPLE_SITE_NO,
         'sample_site_no':  SAMPLE_SITE_NO     
         })
        DF_INFO = pd.concat([DF_INFO, DF_INFO2], ignore_index = False, axis=0) 
        
    return DF_633, DF_785, DF_WN_OTHER_633, DF_WN_OTHER_785, DF_INFO    
 
# %% Sort the othewr wavenumbers before sending for standardisation
   
def process_df_other(df1, df2, df_info ):
    # TODO: check lengths of all wns and determine the shortest OR most common?
    # TODO: process all extra df_others and jusyt get aa full df 633 and 785 for that CNT reaction
    # check is nan in the df other - this will tell you if its just one other wn or many 
    # work with 633 first 
    df2_filter_wn =  df2.filter(regex='^W') # change regex if needed 
    df2_filter_I =  df2.filter(regex='^TT') 
    wn_equal_equality_check = df2_filter_wn.nunique(axis=1).eq(1).all()
    if wn_equal_equality_check: 
    #if not DF_633.isnull().values.any():# if this is true there is only one other wn to deal with -> unless theyre the same lenght but have different values :/
        # check wether df_633 is global or not etc... in this function
        # check if df1 is bigger -> if so send in this order, otherwise, reverse
        df2 = df2_filter_I.set_index(df2_filter_wn.iloc[:,0])
        df_standardized = wavenumber_standardization(df1, df2)
    else:
         wn_quantity = df2_filter_wn.nunique(axis=1) # check this
         wn_groups = df2_filter_wn.T.duplicated() # 1st instance of a thing is False , every instaance there after is True until next OG is false
         for num, col in enumerate(df2_filter_wn.columns):
            try:
                if not wn_groups[num] & wn_groups[num+1]: # this should run when both are false 
                    id_name = col.removeprefix("W")
                    df_to_standardize = pd.concat([df2_filter_wn[col], df2[id_name] ],axis = 1, join='outer', ignore_index=False)
                    df_to_standardize.set_index(df_to_standardize[col], inplace=True)
                    df_standardized = wavenumber_standardization(df1, df_to_standardize)
                    df2.drop([col, id_name], axis=1, inplace=True)  
                    
                else: 
                    # this means theres a duplicate
                    # check how many 
                    next_false_idx = [i for i in range(num + 1, len(wn_groups)) if not wn_groups[i]]
                    col_names = df2_filter_wn.iloc[:, num:next_false_idx-1].columns
                    ids = [i.removeprefix("W") for i in col_names]
                    df_to_standardize = pd.concat([df2_filter_wn[col],df2[ids] ],axis = 1, join='outer', ignore_index=False )
                    df_to_standardize.set_index(df_to_standardize[col], inplace=True)
                    df_strandardized = wavenumber_standardization(df1, df_to_standardize)
                    df2.drop([col_names, ids], axis=1, inplace=True) 
                    df2_filter_wn.drop(col_names)
                    # grab all the id names
                    # then remove the ids involved from both df2_filter_wn and wn_groups so it doesnt fuck you up or skip those rounds in the for loop 
                     
                    
            except IndexError():
                pass
            
            
                    
                 # is the one next to it also false  ->> if yes then its a df of one col to be standardize so build it
            
             
             
         
        # come up with a straategy for if theres a few diferent wavenumbers -> try group which are equal and send through in groups 
        
    
    

    return df_standardized



# %% wave number interpolation needed for below
def wavenumber_standardization(df1, df2):
    # interpolate and find function for all points in OG df 
    # check for duplicates becuase i think there are some here
    # then esitmate new y co-ords for the wavenumber from df_b
    # check and add to df_b
    # repeat for a left over df if there is one
    # TODO: change so that the index of teh dataa fraame (now the wn ) is call as the x value
    # TODO: check which wavenumber has most common
    # TODO: then check the span of x i.e. firsty and last points - > what to do if you're trying to interpolate outside the range

    #check if all df2_filter_wn are equal
    # check if df1>df2_filtered_I
    if df1.shape[1]>= df2.shape[1]:
        df_OG = df1
        df_standardize = df2
    else:
        df_OG = df2
        df_standardize = df1
        
        
    x_OG = df_OG.index
    x_changing = df_standardize.index
    # check which is larger 
    
    col_num=len(df_standardize.columns)
    df3 =pd.DataFrame()
    #df2 =df2.drop(["Wave_num"], axis=1)
    plt.figure()
    for col in df_standardize:
        
        f = interp1d(x_changing, df_standardize[col], kind= "cubic", bounds_error=False, fill_value="extrapolate")
        f_compare = interp1d(x_changing, df_standardize[col], kind= "cubic", bounds_error=False, fill_value="array_like") # compare where there are NaNs to show which values have been extraapolated
        y_new = f(x_OG)        
        
        plt.plot(x_changing, df_standardize[col], 'ob', label = 'measured data')
        plt.plot(x_OG, y_new, '--r', label="Interpolated data")
        plt.xlabel("Wavenumber")
        plt.ylabel("Intensity")
        plt.title("Interpolated wavenumber")
        plt.legend(loc="upper right")
        
        #col_num+=1
        #df3[col] = pd.DataFrame({col:y_new})
        df_new = pd.DataFrame({col:y_new})
        df_new.set_index(df_OG.index, inplace=True)
        df_OG = df_OG.join(df_new, how='left')
        df_OG.index.name = "W"
        #df_OG = pd.concat([df_OG, pd.DataFrame({col:y_new})], ignore_index = False, axis =1 )
        #df2.insert(col_num, col, y_new)
        
    return df_OG
        
def add_to_final_df(df1, df2, df_info, last_num): 
    if df1.empty:
        df1 = df2
    else:
        if df1.index.equals(df2.index):
            # create dicts mapping old to new names 
            df2, df_info = update_info_names(df1, df2, df_info, last_num)
            df1 = df1.join(df2, how='left')
        else:
            
            df2, df_info = update_info_names(df1, df2, df_info, last_num)
            df1 = wavenumber_standardization(df1, df2)
            
    
    return df1,df_info

def update_info_names(df1, df2, df_info, last_num):
    # create dicts mapping old to new names 
    col_names1 = df1.columns[-1] # should address the last id recorded
    #last_num = int(col_names1.removeprefix("TT-R-"))
    col_names2 = df2.columns
    old_nums = [int(i.removeprefix("TT-R-")) for i in col_names2]
    new_nums = [i+last_num for i in old_nums]
    new_ids = ["TT-R-"+"{:03d}".format(i) for i in new_nums]
    #names = [col_names2, new_ids]
    name_dict = dict(zip(col_names2, new_ids))
    for item in col_names2:
        
        df_info.loc[df_info['item_ID'] == item, 'item_ID'] = name_dict[item]
        
        df2.rename(columns = {item: name_dict[item]},  inplace = True)
                              
    return df2, df_info
def save_df_to_csv(df, fp, fn):
    df.to_csv(Path(fp,fn)) 