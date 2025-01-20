#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 10:15:09 2024

@author: laurajodea
"""

import pandas as pd
# %% define file paths 
FILE_PATHS = {
    'READ_RAMAN': '\\Users\\laurajodea\\Documents\\Raman\\RamanProcessSpectras-main\\RawRamanData\\',
    'SAVE_DFS': '\\Users\\laurajodea\\Documents\\Raman\\RamanProcessSpectras-main\\IntermediateDataFrames\\',
    'SAVE_EXCEL': '\\Users\\laurajodea\\Documents\\Raman\\RamanProcessSpectras-main\\ExcelFiles\\'
}

# %% Initialise empty variables 

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