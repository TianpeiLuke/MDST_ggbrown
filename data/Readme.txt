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


10-16-2015
   1. Identify the all nan columns in list_all_nan.csv
   2. Identify the columns in which all items are unique in outlier_freq_str.csv
   3. Count the top 4 most frequent items in each non-numerical/non-time columns (if unique items < 4, then choose unique items + NA). The list stored in list_common_str4.csv