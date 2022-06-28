# -*- coding: utf-8 -*-
"""
Created on Sat May 25 23:11:03 2022

@author: talha
"""

from IPython.display import display  
from sklearn.model_selection import train_test_split, cross_val_predict, KFold
from yellowbrick.model_selection import cv_scores
from tensorflow.keras.models import Sequential
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score
from sklearn import metrics
from tensorflow.keras.layers import LSTM, Dense, Embedding, Dropout, SimpleRNN
import matplotlib.pyplot as plt
import seaborn
import pandas as pd
import time
import pickle
import numpy as np


def ann():
    model = Sequential()
    model.add(Dense(128, input_shape=(6,1), kernel_initializer='normal', activation='relu'))
    model.add(Dense(256, kernel_initializer='normal', activation='relu'))
    model.add(Dense(64, kernel_initializer='normal', activation='relu'))
    model.add(Dense(32, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    model.compile(loss='mean_absolute_error', optimizer="Adam")
    return model

def rnn():
    model = Sequential()
    model.add(SimpleRNN(128,return_sequences=True, input_shape=(6,1)))
    model.add(SimpleRNN(512,return_sequences=False))
    model.add(Dense(64))
    model.add(Dense(1))
    model.compile(optimizer="Adam", loss="mean_absolute_error")
    return model

def save(filename,model):
    pickle.dump(model, open(filename, 'wb'))
    

def run(pathData,pathData_reelTest,pathOut):
    useCols = ["ema_diff_9","sma200","rsi","adx","dx","historyClose","tomorrow","expected"]
    data_df = pd.read_csv(pathData,on_bad_lines='skip',usecols=useCols)
    data_df_reelTest = pd.read_csv(pathData_reelTest,on_bad_lines='skip',usecols=useCols)
    
    display(data_df.head())
    display(data_df.isnull().sum())
    display(data_df.describe())
    
    #"""
    plt.figure(figsize=(16, 8))
    seaborn.heatmap(data_df.corr(), annot=True, fmt='.3f')
    
    pd.DataFrame(data_df.values, columns=data_df.columns).hist()
    plt.tight_layout()
    plt.show()
    
    y_Reel = data_df_reelTest["tomorrow"]
    x_Reel = data_df_reelTest.drop("expected", axis=1)
    x_Reel = x_Reel.drop('tomorrow', axis = 1)
    
    y = data_df["tomorrow"]
    x = data_df.drop('expected', axis = 1)
    x = x.drop('tomorrow', axis = 1)
    
    """
    pca = PCA(n_components=6)
    x = pca.fit_transform(x)
    #"""
    
    """
    scaler = MinMaxScaler(feature_range=(0,1))
    x = scaler.fit_transform(x)
    #"""
    
    """
    scaler = StandardScaler(x)
    x = scaler.transform(x)
    #"""
    
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)
    
    """
    X_train = np.array(X_train)
    X_test = np.array(X_test)
    X_train = np.reshape(X_train, (X_train.shape[1],1))
    X_test  = np.reshape(X_test, (X_test.shape[1],1))
    #"""
    
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    
    data = ""
    #"""
    print("\nLinear Regression:")
    data += "\n\nLinear Regression:"
    start = time.time()
    logreg = LinearRegression()
    logreg.fit(X_train, y_train)
    visualizer = cv_scores(logreg, x, y, cv=cv, scoring='r2')
    scores = np.array(visualizer.cv_scores_)
    print("Mean: ",scores.mean())
    print("SD: ", scores.std())
    data += "\nR2: "
    data += "\nMean: " + str(scores.mean())
    data += "\nSD: " + str(scores.std())
    visualizer = cv_scores(logreg, x, y, cv=cv, scoring='neg_median_absolute_error')
    scores = np.array(visualizer.cv_scores_)
    print("Mean: ",scores.mean())
    print("SD: ", scores.std())
    y_pred = logreg.predict(X_test)
    print("R2: ",metrics.r2_score(y_test, y_pred))
    print("MAE: ",metrics.mean_absolute_error(y_test, y_pred))
    print("MSE: ",metrics.mean_squared_error(y_test, y_pred))
    print("RMSE: ",np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    data += "\nNMAE: "
    data += "\nMean: " + str(scores.mean())
    data += "\nSD: " + str(scores.std())
    data += "\nR2: " + str(metrics.r2_score(y_test, y_pred))
    data += "\nMAE: " + str(metrics.mean_absolute_error(y_test, y_pred))
    data += "\nMSE: " + str(metrics.mean_squared_error(y_test, y_pred))
    data += "\nRMSE: " + str(np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    save("LR_model.sav",logreg)
    
    pred_Reel = logreg.predict(x_Reel)
    plt.plot(pred_Reel,color="r")
    plt.plot(y_Reel,color="b")
    plt.title('LR Reel Predict')
    plt.ylabel("price")
    plt.xlabel('hours')
    plt.legend(['pred', 'reel'], loc='upper left')
    plt.show()
    
    print("Time: ",time.time()-start)
    data += str(time.time()-start)
    
    print("\nDecision Tree Regression:")
    data += "\n\nDecision Tree Regression:"
    start = time.time()
    decision_tree = DecisionTreeRegressor(max_depth=500)
    decision_tree = decision_tree.fit(X_train, y_train)
    visualizer = cv_scores(decision_tree, x, y, cv=cv, scoring='r2')
    scores = np.array(visualizer.cv_scores_)
    print("Mean: ",scores.mean())
    print("SD: ", scores.std())
    data += "\nR2: "
    data += "\nMean: " + str(scores.mean())
    data += "\nSD: " + str(scores.std())
    visualizer = cv_scores(decision_tree, x, y, cv=cv, scoring='neg_median_absolute_error')
    scores = np.array(visualizer.cv_scores_)
    print("Mean: ",scores.mean())
    print("SD: ", scores.std())
    y_pred  = decision_tree.predict(X_test)
    print("R2: ",metrics.r2_score(y_test, y_pred))
    print("MAE: ",metrics.mean_absolute_error(y_test, y_pred))
    print("MSE: ",metrics.mean_squared_error(y_test, y_pred))
    print("RMSE: ",np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    data += "\nNMAE: "
    data += "\nMean: " + str(scores.mean())
    data += "\nSD: " + str(scores.std())
    data += "\nR2: " + str(metrics.r2_score(y_test, y_pred))
    data += "\nMAE: " + str(metrics.mean_absolute_error(y_test, y_pred))
    data += "\nMSE: " + str(metrics.mean_squared_error(y_test, y_pred))
    data += "\nRMSE: " + str(np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    save("DT_model.sav",decision_tree)
    
    pred_Reel = decision_tree.predict(x_Reel)
    plt.plot(pred_Reel,color="r")
    plt.plot(y_Reel,color="b")
    plt.title('DT Reel Predict')
    plt.ylabel("price")
    plt.xlabel('hours')
    plt.legend(['pred', 'reel'], loc='upper left')
    plt.show()
    
    print("Time: ",time.time()-start)
    data += str(time.time()-start)
    
    
    print("\nRandom Forest Regression:")
    data += "\n\nRandom Forest Regression:"
    start = time.time()
    rf = RandomForestRegressor(n_estimators = 500)
    rf.fit(X_train, y_train)
    visualizer = cv_scores(rf, x, y, cv=cv, scoring='r2')
    scores = np.array(visualizer.cv_scores_)
    data += "\nR2: "
    data += "\nMean: " + str(scores.mean())
    data += "\nSD: " + str(scores.std())
    print("Mean: ",scores.mean())
    print("SD: ", scores.std())
    visualizer = cv_scores(rf, x, y, cv=cv, scoring='neg_median_absolute_error')
    scores = np.array(visualizer.cv_scores_)
    print("Mean: ",scores.mean())
    print("SD: ", scores.std())
    y_pred = rf.predict(X_test)
    print("R2: ",metrics.r2_score(y_test, y_pred))
    print("MAE: ",metrics.mean_absolute_error(y_test, y_pred))
    print("MSE: ",metrics.mean_squared_error(y_test, y_pred))
    print("RMSE: ",np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    data += "\nNMAE: "
    data += "\nMean: " + str(scores.mean())
    data += "\nSD: " + str(scores.std())
    data += "\nR2: " + str(metrics.r2_score(y_test, y_pred))
    data += "\nMAE: " + str(metrics.mean_absolute_error(y_test, y_pred))
    data += "\nMSE: " + str(metrics.mean_squared_error(y_test, y_pred))
    data += "\nRMSE: " + str(np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    save("RF_model.sav",rf)
    
    pred_Reel = rf.predict(x_Reel)
    plt.plot(pred_Reel,color="r")
    plt.plot(y_Reel,color="b")
    plt.title('RF Reel Predict')
    plt.ylabel("price")
    plt.xlabel('hours')
    plt.legend(['pred', 'reel'], loc='upper left')
    plt.show()
    
    print("Time: ",time.time()-start)
    data += str(time.time()-start)
    
    
    model = ann()
    data += "\n\nANN:"
    start = time.time()
    history = model.fit(X_train,y_train,validation_data=(X_test,y_test),epochs=20)
    
    print("\nANN")
    y_preds = model.predict(X_test)
    y_pred = y_preds[:,5]
    #y_pred = scaler.inverse_transform(pred)
    
    print("R2: ",metrics.r2_score(y_test, y_pred))
    print("MAE: ",metrics.mean_absolute_error(y_test, y_pred))
    print("MSE: ",metrics.mean_squared_error(y_test, y_pred))
    print("RMSE: ",np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    data += "\nR2: " + str(metrics.r2_score(y_test, y_pred))
    data += "\nMAE: " + str(metrics.mean_absolute_error(y_test, y_pred))
    data += "\nMSE: " + str(metrics.mean_squared_error(y_test, y_pred))
    data += "\nRMSE: " + str(np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    model.save("ANN_model.h5")
    print(time.time()-start)
    data += str(time.time()-start)
    
    plt.plot(history.history['loss'])
    plt.title('ANN train loss')
    plt.ylabel('mean_absolute_error')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()
    
    plt.plot(history.history['val_loss'])
    plt.title('ANN val loss')
    plt.ylabel('mean_absolute_error')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()
    
    pred_Reel = model.predict(x_Reel)
    print(pred_Reel)
    plt.plot(pred_Reel[:,5],color="r")
    plt.plot(y_Reel,color="b")
    plt.title('ANN Reel Predict')
    plt.ylabel("price")
    plt.xlabel('hours')
    plt.legend(['pred', 'reel'], loc='upper left')
    plt.show()
    
    
    model = rnn()
    start = time.time()
    history = model.fit(X_train,y_train,validation_data=(X_test,y_test),epochs=20)
    
    print("\nRNN")
    data += "\n\nRNN:"
    y_pred = model.predict(X_test)
    #y_pred = scaler.inverse_transform(pred)
    print("R2: ",metrics.r2_score(y_test, y_pred))
    print("MAE: ",metrics.mean_absolute_error(y_test, y_pred))
    print("MSE: ",metrics.mean_squared_error(y_test, y_pred))
    print("RMSE: ",np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    data += "\nR2: " + str(metrics.r2_score(y_test, y_pred))
    data += "\nMAE: " + str(metrics.mean_absolute_error(y_test, y_pred))
    data += "\nMSE: " + str(metrics.mean_squared_error(y_test, y_pred))
    data += "\nRMSE: " + str(np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    model.save("RNN_model.h5")
    print(time.time()-start)
    data += str(time.time()-start)
    
    plt.plot(history.history['loss'])
    plt.title('RNN train loss')
    plt.ylabel('mean_absolute_error')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()
    
    plt.plot(history.history['val_loss'])
    plt.title('RNN val loss')
    plt.ylabel('mean_absolute_error')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()
    
    pred_Reel = model.predict(x_Reel)
    plt.plot(pred_Reel,color="r")
    plt.plot(y_Reel,color="b")
    plt.title('RNN Reel Predict')
    plt.ylabel("price")
    plt.xlabel('hours')
    plt.legend(['pred', 'reel'], loc='upper left')
    plt.show()
    
    txt = open(pathOut,"w")
    txt.write(data)
    txt.close()
 
    print("\nfinished")


pathData = r'data_d.csv'
pathData_reelTest = r'data_d_test.csv'
pathOut = "result_d.txt"
run(pathData, pathData_reelTest,pathOut)

pathData = r'data_h.csv'
pathData_reelTest = r'data_h_test.csv'
pathOut = "result_h.txt"
run(pathData, pathData_reelTest,pathOut)

