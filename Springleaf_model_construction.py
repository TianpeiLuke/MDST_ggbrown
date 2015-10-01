#import Springleaf_data_preprocessing

import xgboost as xgb
import scipy.sparse
import pickle


nline_trn = 145232
nline_tst = 145233
nBatch = 20000
rlist = range(np.ceil(float(nline_trn)/float(nBatch)).astype(int)) 
Y = pd.read_csv('./data/train_label.csv')
y_train = Y.values # read training labels
for i in rlist:
    #read training data
    if i == 0:
        train = pd.read_csv("./data/train_cleaned.csv", nrows=nBatch)
    else: 
        train = pd.read_csv("./data/train_cleaned.csv", nrows=nBatch,
                            skiprows= range(1,i*nBatch+1))
   
   



