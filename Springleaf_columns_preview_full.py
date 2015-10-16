# coding: utf-8
# This scipt is for preview the columns and collect the feature statistics


import numpy as np
from numpy import nan as NA
from pandas import Series, DataFrame
import pandas as pd
import re
from collections import Counter
import csv
import time

nline_trn = 145232
nline_tst = 145233
nBatch = 20000

ifstore = True
y_train = np.zeros([nline_trn, 1])
#rlist = range(np.ceil(float(nline_trn)/float(nBatch)).astype(int)) 
#for i in rlist:
#reading data in batches
#    if i == 0:
train = pd.read_csv("./data/train.csv")
#    else: 
#        train = pd.read_csv("./data/train.csv", nrows=nBatch,
#                            skiprows= range(1,i*nBatch+1))
nrows = len(train.index)
ncols = len(train.columns)
   
train.drop(['ID', 'target'], axis=1, inplace = True)
#  for each column, make a summary of elements, stored in info_num, info_char

def isTimeFormat(input):
    try:
        time.strptime(input, '%d%b%y:%H:%M:%S')
        return True
    except ValueError:
        return False
#    if i == 0:
info_num = {}
info_char = {}
info_count_str = {}
des_series = {}
all_nan = {}

print("\n Data summarization...")
for j, c in enumerate(train):
    trn_na = train[c].dropna(axis = 0)
    if len(trn_na) == 0:
       print('The all nan column name: ' + c)
       all_nan[c] = train[c].unique()
    elif not np.isreal(train[c][train[c].first_valid_index()]):
       train[c][train[c] == "-1"] = NA
       train[c][train[c] == "[]"] = NA
       train[c][train[c] == ""] = NA
       train[c][train[c] == -1] = NA
            #string elements to find unique strings
#            if i == 0:
       trn_na_more = train[c].dropna(axis = 0)
       if len(trn_na_more) == 0:
           print('The all nan column name'+ c)
           all_nan[c] = train[c].unique()
       else:
           info_char[c] = sorted(train[c].unique())
       #find the 1-4th most common strings
           print(j,c, train[c].unique())
#            else:
#               temp_char = np.concatenate((info_char[c],
#                                               train[c].unique()), axis= 0)
#               info_char[c] = np.unique(temp_char)
#               print(j, c, info_char[c])
    else:  #numerical elements to make summary
        print(j, c, "Numeric")
#       if i == 0:
        print(train[c].describe())
        info_num[c] = train[c].describe()
 #      else: 
 #           des_series = train[c].describe()
 #           org_series = info_num[c]
 #           if len(train[c].describe()) == 4: #train[c][0] == False or train[c][0] == True:
              #count sum
#                des_series[0] = des_series[0] + org_series[0]
#                des_series[1] = np.max([des_series[1], org_series[1]])
              #count most freq items
#                if des_series[2] != org_series[2]:
#                    if des_series[3] < org_series[3]:
#                       des_series[3] = org_series[3]
#                       des_series[2] = org_series[2]
#                else:
#                     if len(des_series.dropna(axis=0)) != len(des_series):
#                           des_series = {}
#                           org_series = {}
#                           continue
#                     #mean sum
#                     des_series[1] = (des_series[1]*des_series[0] + org_series[1]*org_series[0])/(org_series[0]+ des_series[0])
#                     #std
#                     des_series[2] = np.sqrt((des_series[0]*des_series[2]**2+org_series[0]*org_series[2]**2 )/(org_series[0]+ des_series[0]))
#                     #min
#                     des_series[3] = np.min([des_series[3], org_series[3]])
#                     #average other quantiles
#                     des_series[4] = (des_series[4]*des_series[0] + org_series[4]*org_series[0])/(org_series[0]+ des_series[0])
#                     des_series[5] = (des_series[5]*des_series[0] + org_series[5]*org_series[0])/(org_series[0]+ des_series[0])
#                     des_series[6] = (des_series[6]*des_series[0] + org_series[6]*org_series[0])/(org_series[0]+ des_series[0])
#                     #max
#                     des_series[7] = np.max([des_series[7], org_series[7]])
#                     #count sum
#                     des_series[0] = des_series[0] + org_series[0]
#                     print(des_series)
#                     #store it
#                     info_num[c] = des_series
#                     des_series = {}
#                     org_series = {}
#
# store the numerical data and result
all_nan_frame = pd.DataFrame(all_nan)
if ifstore == True:
    print("\nnum of nan columns: %d" % len(all_nan.keys()))
    all_nan_frame.to_csv('./data/all_nan_summary.csv', index= False)
summary_num = pd.DataFrame(info_num)
if ifstore == True:
    print("\nConvert summary into csv file...")
    summary_num.to_csv('./data/train_num_summary.csv', index = False)
time_dict = {}
string_dict = {}

is_time = 0
if ifstore == True:
  w = csv.writer(open("./data/info_num.csv", "w"))
  for key, val in info_num.items():
      w.writerow([key, val])
if ifstore == True:
   w = csv.writer(open("./data/info_char.csv", "w"))
for key, val in info_char.items():
    is_time = 0
    is_first_nan = 0
    if ifstore == True:
       w.writerow([key, val])
   # if len(val)>1 and isTimeFormat(val[1]):
   #     is_time = 1
    if np.isreal(val[0]) and np.isnan(val[0]):
        is_first_nan = 1
        if len(val)>1 and is_first_nan == 0 and isTimeFormat(val[0]):
           is_time = 1
        elif len(val)>1 and is_first_nan == 1 and isTimeFormat(val[1]):
           is_time = 1
    string_dict[key] = pd.Series([len(val), is_first_nan, is_time], index= ['len(unique)', 'is_first_nan', 'is_time'])

summary_str = pd.DataFrame(string_dict)
if ifstore == True:
    summary_str.to_csv('./data/summary_str.csv', index= False)
#=================================================================
#   outlier extraction
print('Outlier extraction')
print("Extract outlier string columns and daytime columns")
outlier_str_dict = {}
time_str_dict = {}
for s in summary_str.columns:
    if summary_str[s][0] <= 2 and summary_str[s][1] == 1:
        outlier_str_dict[s] = info_char[s]
    elif summary_str[s][2] == 1:
        time_str_dict[s] = summary_str[s]
outlier_str = pd.DataFrame.from_dict(outlier_str_dict, orient= 'index').T
time_str_df = pd.DataFrame(time_str_dict)
if ifstore == True:
    time_str_df.to_csv('./data/time_col_list.csv', index = False)
    outlier_str.to_csv('./data/outlier_str_list.csv', index= False)

#frequency count
string_freq_outlier = {}
list_tuple = []
print('Count frequency')
for j, c in enumerate(train):
    if c in outlier_str.columns: #skip those only occur once
       continue
    trn_na = train[c].dropna(axis = 0)
    if (len(trn_na) > 0) and (not np.isreal(train[c][train[c].first_valid_index()])):
       train[c][train[c] == "-1"] = NA
       train[c][train[c] == "[]"] = NA
       train[c][train[c] == ""] = NA
       train[c][train[c] == -1] = NA
            #string elements to find unique strings
#            if i == 0:
       trn_na_more = train[c].dropna(axis = 0)
       if len(trn_na_more) > 0:
           if isTimeFormat(train[c][train[c].first_valid_index()]) == False: 
               print('Contruct counter for %s ...' % c)
               counter = Counter(train[c].dropna(axis= 0))
               list_tuple = counter.most_common(np.min([len(train[c].dropna(axis = 0).unique()), 4]))
               type_list = [NA, NA, NA, NA]
               type_list[:len(list_tuple)]= [T[0] for T in list_tuple]
               if list_tuple[0][1] == 1:
                     #record the columns in which each item only occur once
                     string_freq_outlier[c] = np.array(type_list, dtype = object)
               else:      
                     info_count_str[c] = np.array(type_list, dtype = object)
               list_tuple = []

str_freq_outlier_pd = pd.DataFrame(string_freq_outlier)
summary_str_com = pd.DataFrame(info_count_str)
print('num column with max frequency 1: %d' % len(str_freq_outlier_pd.columns))
if ifstore == True:
    summary_str_com.to_csv('./data/train_common_str4.csv', index = False)    
    str_freq_outlier_pd.to_csv('./data/outlier_freq_str.csv', index= False)



# numerical values
count = 0
outlier_dict = {}
outlier_bool = {}
suspect_dict = {}
sparse_dict = {}
large_dict = {}
negative_dict = {}
'''
The entities for summary_num
[0] 25%      quantile
[1] 50%      median
[2] 75%      ...
[3] count    number of elements in count
[4] freq     for boolean, freq of largest element
[5] max      maximum element
[6] mean     mean values 
[7] min      minimum element
[8] std      standard deviation
[9] top      for boolean, most frequent element
[10] unique  for boolean, number of unique elements
'''
print("Extract outlier numerical columns")
for c in summary_num.columns:
    if (not np.isnan(summary_num[c][4])) and (summary_num[c][10] == 1):
       outlier_bool[c] = summary_num[c][[4,9,10]]
    if (np.isnan(summary_num[c][4])) and (abs(summary_num[c][2]/summary_num[c][0]) > 1e3):
       suspect_dict[c] = summary_num[c]
    if (summary_num[c][0] > 9990) and (np.absolute(summary_num[c][0]- summary_num[c][5])<= 5) or ((summary_num[c][2] < -9990) and (np.absolute(summary_num[c][7]- summary_num[c][2])<= 5)):
       outlier_dict[c] = summary_num[c][[0,5]] 
    elif np.log10(abs(summary_num[c][5]- summary_num[c][7])) > 5 :
       large_dict[c] = summary_num[c][[0,1,2,5,6,7]] 
    if summary_num[c][2] == summary_num[c][0] and summary_num[c][2] == 0 :
       sparse_dict[c] = summary_num[c][[0,1,2,5,6,7]]
    if summary_num[c][7] < 0 and summary_num[c][7] > -9990:
       negative_dict[c] = summary_num[c][[0,1,2,5,6,7]]

outlier_num = pd.DataFrame(outlier_dict)
outlier_bool_pd = pd.DataFrame(outlier_bool)
suspect_num = pd.DataFrame(suspect_dict)
sparse_num = pd.DataFrame(sparse_dict)
large_num = pd.DataFrame(large_dict)
negative_num = pd.DataFrame(negative_dict)
if ifstore == True:
   print('Store back...')
   outlier_num.to_csv('./data/outlier_list.csv', index = False)
   outlier_bool_pd.to_csv('./data/outlier_bool_list.csv', index = False)
   suspect_num.to_csv('./data/large_gap_list.csv', index = False)
   sparse_num.to_csv('./data/sparse_list.csv', index = False)
   large_num.to_csv('./data/large_list.csv', index = False)
   negative_num.to_csv('./data/negative_list.csv', index = False)
