This is for SpringLeaf competition in Kaggle
see www.kaggle.com/c/springleaf-marketing-response

Name of team: ggbrown
Member:  Tianpei, Xinyu,  Xiang, Jianming.


======================================================================================
Logs
by Tianpei Xie

09-30-2015
   1. Summary of whole data, ready in list_summary_num.csv
   2. Identify the outlier numerical features by checking the difference of 25% and maximum feature values
   3. Identify the outlier bool features by checking the number of unique values 
   4. The outlier list in outlier_num.csv, outlier_bool.csv

10-01-2015
   1. Summary of string data, includes the number of unique strings
   2. Identify the time data with list in list_time.csv
   3. Identify large gaps in numerical columns btw 25% and 75% data, in list_large_gap.csv
   4. Identify the string columns with only nan and one string, in outlier_str.csv
   5. Change the Springleaf_data_preprocessing_total.py. It now encodes the day/month/year/time into three different features: ‘orgname’ = (year-2010)*12+ month, and ‘orgname’+y = year-2010; and ‘orgname’+ month = month
   6. Identify the columns with 999999 and -999999 or 1x1E9 items in list_large_item.csv
   7. Identify the columns with fewer than 25% nonzero in list_sparse.csv
    
    see https://github.com/TianpeiLuke/MDST_ggbrown/tree/master/data

10-04-2015
   To do list: 
   1. Change -1 to NA in train data (lots of them) (Tianpei)
   2. Columns with 1e9 (to NA or log) (Tianpei)
   3. Tune boosting parameters (Xiang)
   4. Bootstrap aggregation (randomly sample data) (Xinyu)
   5. Write xgboost in Python (Tianpei)

10-08-2015
   Progress meeting
   1. log transformation of data didn’t work
   2. NaN transformed to -99999 is working (transformed to mean didn’t work)

10-09-2015 
   To-do list
   1. parameter tuning
   2. feature selection
   3. debug (target has 1 more column than train)


10-16-2015
   1. Identify the all nan columns in list_all_nan.csv
   2. Count the top 4 most frequent items in each non-numerical/non-time columns
      stored in list_common_str4.csv
   3. Identify the items with all items distinct (max freq for each item = 1) in outlier_freq_str.csv
   4. Convert the top 4 most frequent items in each string column and stored back; code in 
      Springleaf_data_preprocessing_trn.py
   5. Do the same process for test data in Springleaf_data_preprocessing_tst.py
   6. New train_cleaned.csv and test_cleaned.csv 

10-17－2015
   1. program for xgboost training with parameter given by Xiyu
   2. R-script in ./src  and Python-script in Springleaf_model_construction.py
   3. Not improve in score (Tianpei submission)
   
