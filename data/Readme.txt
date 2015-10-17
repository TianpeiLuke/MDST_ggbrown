09-30-2015
   1. Summary of whole data, ready in train_num_summary.csv
   2. Identify the outlier numerical features by checking the difference of 25% and maximum feature values
   3. Identify the outlier bool features by checking the number of unique values 
   4. The outlier list in outlier_list.csv, outlier_bool_list.csv

10-01-2015
   1. Summary of string data, includes the number of unique strings
   2. Identify the time data with list in time_col_list.csv
   3. Identify large gaps in numerical columns btw 25% and 75% data, in large_gap_list.csv
   4. Identify the string columns with only nan and one string, in outlier_str_list.csv
   5. Change the Springleaf_data_preprocessing_total.py. It now encodes the day/month/year/time into three different features: ‘orgname’ = (year-2010)*12+ month, and ‘orgname’+y = year-2010; and ‘orgname’+ month = month

10-16-2015
   1. Identify the all nan columns in all_nan_summary.csv
   2. Identify the columns in which all items are unique in outlier_freq_str.csv
   3. Count the top 4 most frequent items in each non-numerical/non-time columns (if unique items < 4, then choose unique items + NA). The list stored in train_common_str4.csv