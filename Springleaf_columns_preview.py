# coding: utf-8
# This scipt is for preview the columns and collect the feature statistics


import numpy as np
from numpy import nan as NA
from pandas import Series, DataFrame
import pandas as pd
import re

nline_trn = 145232
nline_tst = 145233
nBatch = 20000
y_train = np.zeros([nline_trn, 1])
rlist = range(np.ceil(float(nline_trn)/float(nBatch)).astype(int)) 
for i in rlist:
#reading data in batches
    if i == 0:
        train = pd.read_csv("./data/train.csv", nrows=nBatch)
    else: 
        train = pd.read_csv("./data/train.csv", nrows=nBatch,
                            skiprows= range(1,i*nBatch+1))

    nrows = len(train.index)
    ncols  = len(train.columns)
   
    train.drop(['ID', 'target'], axis=1, inplace = True)
    if i == 0:
        info_num = {}
        info_char = {}
    des_series = {}
    org_series = {}
    print("\n Data summarization...")
    for j, c in enumerate(train):
        trn_na = train[c].dropna(axis = 0)
        if len(trn_na) == 0:
           continue
        if not np.isreal(train[c][train[c].first_valid_index()]):
            if i == 0:
               info_char[c] = train[c].unique()
               print(j,c, train[c].unique())
            else:
               temp_char = np.concatenate((info_char[c],
                                               train[c].unique()), axis= 0)
               info_char[c] = np.unique(temp_char)
               print(j, c, info_char[c])
        else:
             print(j, c, "Numeric")
             if i == 0:
                print(train[c].describe())
                info_num[c] = train[c].describe()
             else: 
                des_series = train[c].describe()
                org_series = info_num[c]
                if len(train[c].describe()) == 4: #train[c][0] == False or train[c][0] == True:
                       #count sum
                     des_series[0] = des_series[0] + org_series[0]
                     des_series[1] = np.max([des_series[1], org_series[1]])
                       #count most freq items
                     if des_series[2] != org_series[2]:
                           if des_series[3] < org_series[3]:
                                des_series[3] = org_series[3]
                                des_series[2] = org_series[2]
                else: 
												if len(des_series.dropna(axis=0)) != len(des_series):
															des_series = {}
															org_series = {}
															continue
												#mean sum
												des_series[1] = (des_series[1]*des_series[0] + org_series[1]*org_series[0])/(org_series[0]+ des_series[0])
												#std
												des_series[2] = np.sqrt((des_series[0]*des_series[2]**2+org_series[0]*org_series[2]**2 )/(org_series[0]+ des_series[0]))
												#min
												des_series[3] = np.min([des_series[3], org_series[3]])
												#average other quantiles
												des_series[4] = (des_series[4]*des_series[0] + org_series[4]*org_series[0])/(org_series[0]+ des_series[0])
												des_series[5] = (des_series[5]*des_series[0] + org_series[5]*org_series[0])/(org_series[0]+ des_series[0])
												des_series[6] = (des_series[6]*des_series[0] + org_series[6]*org_series[0])/(org_series[0]+ des_series[0])
												#max
												des_series[7] = np.max([des_series[7], org_series[7]])
												#count sum
												des_series[0] = des_series[0] + org_series[0]
												print(des_series)
												#store it
												info_num[c] = des_series
												des_series = {}
												org_series = {}
            
                
# store the data and result
summary_num = pd.DataFrame(info_num)
summary_num.to_csv('./data/train_num_summary.csv')
import csv
w = csv.writer(open("./data/info_num.csv", "w"))
for key, val in info_num.items():
    w.writerow([key, val])
w = csv.writer(open("./data/info_char.csv", "w"))
for key, val in info_char.items():
    w.writerow([key, val])
#=================================================================

count = 0
outlier_dict = {}
for c in summary_num.columns:
    if (summary_num[c][0] > 9990) and (np.absolute(summary_num[c][0]- summary_num[c][5])<= 5) :
       outlier_dict[c] = summary_num[c][[0,5]]

outlier_num = pd.DataFrame(outlier_dict)
outlier_num.to_csv('./data/outlier_list.csv')




