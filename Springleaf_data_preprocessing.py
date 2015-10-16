# coding: utf-8

# Python script for Springleaf data preprocessing
# https://www.kaggle.com/c/springleaf-marketing-response
# modify to load the whole data
# In[137]:

import numpy as np
from numpy import nan as NA
from pandas import Series, DataFrame
import pandas as pd


nline_trn = 145232 - 1
nline_tst = 145233 - 1
nBatch = 20000
y_train = np.zeros([nline_trn, 1])
# read the outlier lists
all_nan  = pd.read_csv('./data/all_nan_summary.csv')
outlier_num = pd.read_csv('./data/outlier_list.csv')
outlier_bool =  pd.read_csv('./data/outlier_bool_list.csv')
outlier_str = pd.read_csv('./data/outlier_str_list.csv')
outlie_frq_str = pd.read_csv('./data/outlier_freq_str.csv')
# read the list of time featurs
time_feature = pd.read_csv('./data/time_col_list.csv')
most_common_str = pd.read_csv('./data/train_common_str4.csv')

print "===================================================="
train = pd.read_csv("./data/train.csv")

nrows = len(train.index)
ncols  = len(train.columns)

print('Row count: %d' % nrows)
print('Column count: %d' % ncols)
print("Row count in total: " +  str(nline_trn))

y_train = train['target']
train.drop(['ID', 'target'], axis=1, inplace = True)


print "\nDrop all nan columns..." 
print "Drop columns with most entities > 9990..."
print "Drop columns with identical boolean and string variables "
train.drop(all_nan.columns, axis = 1, inplace = True)
train.drop(outlier_num.columns, axis=1, inplace = True)
train.drop(outlier_bool.columns, axis=1, inplace = True)
train.drop(outlier_str.columns, axis = 1, inplace = True)
train.drop(outlier_frq_str.columns, axis = 1, inplace = True)
print "Column count: %d"  % len(train.columns)

train_num = train.select_dtypes(include=[np.number])
train_char = train.select_dtypes(include=[object])
print("Numerical column count : "+ str(len(train_num.columns))+ "; Character column count : "+ str(len(train_char.columns)))

print "Replace -1, [], empty as nan"
train_char[train_char=="-1"] = NA
train_char[train_char==""] = NA
train_char[train_char=="[]"] = NA

# We place the date columns in a new dataframe and parse the dates
print "Parse the date"
train_date = train[time_feature.columns]
train_char.drop(time_feature.columns, axis = 1, inplace = True)

for c in train_date.columns:
       train_date[c+ 'm']= (pd.to_datetime(train_date[c],format ='%d%b%y:%H:%M:%S').map(lambda x: x.month))
       train_date[c+ 'y']= (pd.to_datetime(train_date[c],format ='%d%b%y:%H:%M:%S').map(lambda x: x.year-2010))
       train_date[c]= (pd.to_datetime(train_date[c],format ='%d%b%y:%H:%M:%S').map(lambda x: (x.year-2010)*12+x.month))

# Maintain the feature ordering
print "Feature stored back...\n"
data_cleaned = train
data_cleaned[train_char.columns.values]= train_char
data_cleaned[train_num.columns.values]= train_num
data_cleaned[train_date.columns.values]= train_date
data_cleaned.to_csv('./data/train_cleaned.csv', index = False)

Y = pd.DataFrame(y_train)
Y.columns = ['Target']
Y.to_csv('./data/train_label.csv', index= False)
#===================================================================


