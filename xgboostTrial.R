library(caret)
library(xgboost)
library(ROCR)

## load data
data_file = 'F:/Xinyu/Google Drive/MDST_GGB/data/train_cleaned.csv'
target_file = 'F:/Xinyu/Google Drive/MDST_GGB/data/train_label.csv'
test_file = 'F:/Xinyu/Google Drive/MDST_GGB/data/test_cleaned.csv'

classes <- read.csv(target_file)
training <- read.csv(data_file)
training["target"] <- classes
testing = read.csv(test_file)

## cross-validation
inTrain <- createDataPartition(training$target, p = 0.7, list = F)
training_c <- training[inTrain, ]
testing_c <- training[-inTrain, ]

dtrain <- xgb.DMatrix(data.matrix(subset(training_c, select=-target)), 
                      label=training_c$target, missing = NA)

gc()

dval <- xgb.DMatrix(data.matrix(subset(testing_c, select = -target)), 
                    label=testing_c$target, missing = NA)

watchlist <- list(eval = dval, train = dtrain)

param <- list(  objective           = "binary:logistic", 
                # booster = "gblinear",
                eta                 = 0.01, # 0.06, #0.01,
                max_depth           = 8, #changed from default of 8
                subsample           = 0.7, # 0.7
                colsample_bytree    = 0.8, # 0.7
                eval_metric         = "auc"
                # alpha = 0.0001, 
                # lambda = 1
)

clf <- xgb.train(   params              = param, 
                    data                = dtrain, 
                    nrounds             = 950, #300, #280, #125, #250, # changed from 300
                    verbose             = 1,
                    #early.stop.round    = 10,
                    watchlist           = watchlist,
                    maximize            = TRUE)


dtrain=0
gc()

dval=0
gc()

dtest <- xgb.DMatrix(data.matrix(subset(testing, select=-ID)), missing = NA) 
submission <- data.frame(ID=testing$ID)
submission$target <- predict(clf, dtest)




cat("saving the submission file\n")
write.csv(submission, "xgb_v2.csv", row.names = F)