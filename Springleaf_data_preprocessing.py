# coding: utf-8

# Python script for Springleaf data preprocessing
# https://www.kaggle.com/c/springleaf-marketing-response

# In[137]:

import numpy as np
from numpy import nan as NA
from pandas import Series, DataFrame
import pandas as pd
import re


# Read training data

# In[138]:

train = pd.read_csv("./data/train.csv", nrows=20000)


# Take a look at the column names

# In[139]:

train.columns


# Drop ID and target

# In[140]:
# Do not drop target
y_train = train['target']
train = train.drop(['ID', 'target'], axis=1)
train.columns


# Get row count and column count

# In[141]:

nrow = len(train.index)
ncol = len(train.columns)
print('Row count: %d' % nrow)
print('Column count: %d' % ncol)


# Count total rows in traing data

# In[156]:

#def countLines(name):
#    file = open(name)
#    nline = len(file.readlines())
#    file.close()
#    return nline
#nline = countLines('./data/train.csv')
nline = 145232 
print("Row count : " +  str(nline) + "; Predictor column count : "+ str(ncol))


# Proportion of NA values

# In[142]:

#1-sum(train.count(axis=1))/(nrow*ncol)


# Check for duplicate rows (there is none)

# In[143]:

#len(train.index) - len((train.drop_duplicates()).index)


# Look at the columns with only one unique value, drop these columns (there are 2 of them)

# In[144]:
print "\nDrop columns with identical entities..."
def funct1(df):
    return len(df.drop_duplicates().index)
col_val_count = train.apply(funct1)
col_val_count
train = train.drop((col_val_count[col_val_count == 1]).index, axis=1)
print "Column count: %d"  % len(train.columns)


# Identify and select numeric and character rows (note the result is different from the Original R script)

# In[147]:

train_num = train.select_dtypes(include=[np.number])
train_char = train.select_dtypes(include=[object])
print("Numerical column count : "+ str(len(train_num.columns))+ "; Character column count : "+ str(len(train_char.columns)))


# Peek into character features
print "\n Process the character data"
# In[178]:

def funct2(df):
    return df.drop_duplicates().tolist()
train_char.apply(funct2)


# It looks like NA is represented in character columns by -1 or [] or blank values, so convert these to explicit NAs. 
# Not entirely sure this is the right thing to do as there are real NA values, as well as -1 values already existing, 
# however it can be tested in predictive performance.

# In[179]:
print "\n Replace -1, [], empty as nan"
train_char[train_char=="-1"] = NA
train_char[train_char==""] = NA
train_char[train_char=="[]"] = NA


# We place the date columns in a new dataframe and parse the dates

# In[218]:
print "\n Parse the date"
def funct3(df):
    return len(df[df.str.contains(r'JAN1|FEB1|MAR1')==True]) > 0
index_date = train_char.apply(funct3)
train_date = train_char[index_date.index[index_date]]
train_char = train_char.drop(train_date.columns, axis=1)
train_date.apply(funct2)


# Map the date to integer from 1 to 12, which represent months

# In[217]:

def funct4(s):
    s[s.str.contains(r'JAN')==True] = 1
    s[s.str.contains(r'FEB')==True] = 2
    s[s.str.contains(r'MAR')==True] = 3
    s[s.str.contains(r'APR')==True] = 4
    s[s.str.contains(r'MAY')==True] = 5
    s[s.str.contains(r'JUN')==True] = 6
    s[s.str.contains(r'JUL')==True] = 7
    s[s.str.contains(r'AUG')==True] = 8
    s[s.str.contains(r'SEP')==True] = 9
    s[s.str.contains(r'OCT')==True] = 10
    s[s.str.contains(r'NOV')==True] = 11
    s[s.str.contains(r'DEC')==True] = 12
train_date.apply(funct4)
train_date.apply(funct2)
train_date

# In[222]:
# Maintain the feature ordering
print "\n Feature stored back"
data_cleaned = train
data_cleaned[train_char.columns.values]= train_char
data_cleaned[train_num.columns.values]= train_num
data_cleaned[train_date.columns.values]= train_date
#data_cleaned = pd.concat([train_num, train_char, train_date])


# In[223]:

data_cleaned.to_csv('./data/train_cleaned.csv')


# In[ ]:



