
# Import Library

library(readxl)
library(glmnet)
library(mice)
library(caret)
library(tidyverse)
library(rpart)
library(randomForest)
library(PerformanceAnalytics)
#install.packages("pls")
library(pls)

######################################################

# Import Data

data <- read_excel("../data/data.xlsx")
View(data)

######################################################

# Data

data$marka <- as.factor(data$marka)
data$ekran_boyutu <- as.factor(data$ekran_boyutu)
data$islemci_marka <- as.factor(data$islemci_marka)
data$ram <- as.factor(data$ram)
data$depolama <- as.factor(data$depolama)
data$ekran_arayuz <- as.factor(data$ekran_arayuz)
data$isletim_sistemi <- as.factor(data$isletim_sistemi)

data$marka <- as.numeric(data$marka)
data$ekran_boyutu <- as.numeric(data$ekran_boyutu)
data$islemci_marka <- as.numeric(data$islemci_marka)
data$ram <- as.numeric(data$ram)
data$depolama <- as.numeric(data$depolama)
data$ekran_arayuz <- as.numeric(data$ekran_arayuz)
data$isletim_sistemi <- as.numeric(data$isletim_sistemi)

data$islemci_hiz <- gsub(",", ".", data$islemci_hiz)
data$agirlik <- gsub(",", ".", data$agirlik)
data$fiyat <- gsub(",", ".", data$fiyat)

data$islemci_hiz <- as.double(data$islemci_hiz)
data$agirlik <- as.double(data$agirlik)
data$fiyat <- as.double(data$fiyat)

data <- na.omit(data)
data <- data[sample(1:nrow(data)), ]


######################################################

# preprocessing data (pca, one hot encoding)

num_cols <- c("agirlik","islemci_hiz","fiyat")
pre_scaled <- preProcess(data[,num_cols], method = c("center","scale"))
dataScaled <- predict(pre_scaled, data)
dataScaled <- as.data.frame(dataScaled)

data_OHE <- model.matrix(fiyat ~ ., data = dataScaled)
data_OHE <- as.data.frame(data_OHE)

set.seed(111)
sampleIndex <- sample(1:nrow(data_OHE),size = 0.8*nrow(data_OHE))

# train data and test data

trainSet_normal <- data[sampleIndex,] # özellik dönüşümü yok
testSet_normal <- data[-sampleIndex,] # özellik dönüşümü yok

trainSet_x <- data_OHE[sampleIndex,]
testSet_x <- data_OHE[-sampleIndex,]

trainSet_y <- dataScaled$fiyat[sampleIndex]
testSet_y <- dataScaled$fiyat[-sampleIndex]
trainSet_y <- as.data.frame(trainSet_y)
testSet_y <- as.data.frame(testSet_y)

trainSet <- dataScaled[sampleIndex,]
testSet <- dataScaled[-sampleIndex,]


#########################################################

# Correlations

#summary(data_OHE)
cor(dataScaled)
chart.Correlation(dataScaled, histogram = TRUE, method = "pearson")

#########################################################

#Regression Model
modelRegression <- pcr(fiyat ~ ., data=trainSet, scale=TRUE, validation="CV")
modelRegression_normal <- lm(fiyat ~ ., data = trainSet) # özellik dönüşümü yok
summary(modelRegression)
summary(modelRegression_normal) # özellik dönüşümü yok

#Regression Prediction and RMSE

predictionsReg <- predict(modelRegression, testSet)
predictionsReg_normal <- predict(modelRegression_normal, testSet) # özellik dönüşümü yok

#########################################################

#Determine the lambda parameter using cross-validation

lambdas = 10^seq(3,-2,by=-.01)

modelRidgeCV <- cv.glmnet(as.matrix(trainSet_x),as.matrix(trainSet_y), alpha = 0, lambda = lambdas, nfolds = 3)

#Ridge Model

modelRidge <- glmnet(as.matrix(trainSet_x),as.matrix(trainSet_y), alpha = 0, lambda = modelRidgeCV$lambda.min)
summary(modelRidge)

# Ridge Prediction 

predictionRidge <- predict(modelRidge, as.matrix(testSet_x))

#########################################################

#Determine the lambda parameter using cross-validation

modelLassoCV <- cv.glmnet(as.matrix(trainSet_x),as.matrix(trainSet_y), alpha = 1, lambda = lambdas, nfolds = 10)

#Lasso Model

modelLasso <- glmnet(as.matrix(trainSet_x),as.matrix(trainSet_y), alpha = 1, lambda = modelLassoCV$lambda.min)
summary(modelLasso)

# Lasso Prediction 

predictionLasso <- predict(modelLasso, as.matrix(testSet_x))

#########################################################

#Regression Tree Model

modelRegTree <- rpart(fiyat ~ ., data=trainSet)
summary(modelRegTree)

#Regression Tree Prediction 

predictionRegTree <- predict(modelRegTree, testSet)

#########################################################

#Random Forest Model

modelRF <- randomForest(fiyat ~ ., data=trainSet, ntree=750)

# Random Forest Prediction 

predictionRF <- predict(modelRF, testSet)

#########################################################

# RESULT
# All RMSE, R2, MAE

Reg_normal_RMSE <- RMSE(predictionsReg_normal, testSet$fiyat) # özellik dönüşümü yok
Reg_normal_R2 <- R2(predictionsReg_normal, testSet$fiyat) # özellik dönüşümü yok
Reg_normal_MAE <- MAE(predictionsReg_normal, testSet$fiyat) # özellik dönüşümü yok
Reg_RMSE <- RMSE(predictionsReg, testSet$fiyat)
Reg_R2 <- R2(predictionsReg, testSet$fiyat)
Reg_MAE <- MAE(predictionsReg, testSet$fiyat)
Ridge_RMSE <- RMSE(predictionRidge, as.matrix(testSet_y))
Ridge_R2 <- R2(predictionRidge, as.matrix(testSet_y))
Ridge_MAE <- MAE(predictionRidge, as.matrix(testSet_y))
Lasso_RMSE <- RMSE(predictionLasso, as.matrix(testSet_y))
Lasso_R2 <- R2(predictionLasso, as.matrix(testSet_y))
Lasso_MAE <- MAE(predictionLasso, as.matrix(testSet_y))
RT_RMSE <- RMSE(predictionRegTree, testSet$fiyat)
RT_R2 <- R2(predictionRegTree, testSet$fiyat)
RT_MAE <- MAE(predictionRegTree, testSet$fiyat)
RF_RMSE <- RMSE(predictionRF, testSet$fiyat)
RF_R2 <- R2(predictionRF, testSet$fiyat)
RF_MAE <- MAE(predictionRF, testSet$fiyat)

Reg_normal_RMSE # özellik dönüşümü yok
Reg_RMSE
Ridge_RMSE
Lasso_RMSE
RT_RMSE
RF_RMSE

Reg_normal_R2 # özellik dönüşümü yok
Reg_R2
Ridge_R2
Lasso_R2
RT_R2
RF_R2


Reg_normal_MAE # özellik dönüşümü yok
Reg_MAE
Ridge_MAE
Lasso_MAE
RT_MAE
RF_MAE

summary(data$fiyat)
summary(testSet$fiyat)
