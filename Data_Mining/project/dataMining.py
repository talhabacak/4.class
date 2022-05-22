# -*- coding: utf-8 -*-
"""
Created on Wed May 18 23:28:34 2022

@author: talha
"""

from IPython.display import display  
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVC
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn
import pandas as pd
import time
import pickle


pathData = r'data/cardioTrain_2.csv'

useCols = ["age","gender","height","weight","ap_hi","ap_lo","cholesterol","gluc","smoke","alco","active","cardio"]
data_df = pd.read_csv(pathData,on_bad_lines='skip',usecols=useCols)

data_df["gender"] = data_df["gender"] - 1

display(data_df.head())
display(data_df.isnull().sum())
display(data_df.describe())
display(data_df['cardio'].value_counts())

plt.figure(figsize=(16, 8))
seaborn.heatmap(data_df.corr(), annot=True, fmt='.3f')

pd.DataFrame(data_df.values, columns=data_df.columns).hist()
plt.tight_layout()

plt.figure(figsize=(16, 8))
plt.hist(data_df["age"])
plt.title("age")
plt.figure(figsize=(16, 8))
plt.hist(data_df["gender"])
plt.title("gender")
plt.figure(figsize=(16, 8))
plt.hist(data_df["height"])
plt.title("height")
plt.figure(figsize=(16, 8))
plt.hist(data_df["weight"])
plt.title("weight")
plt.figure(figsize=(16, 8))
plt.hist(data_df["ap_hi"])
plt.title("ap_hi")
plt.figure(figsize=(16, 8))
plt.hist(data_df["ap_lo"])
plt.title("ap_lo")
plt.figure(figsize=(16, 8))
plt.hist(data_df["cholesterol"])
plt.title("cholesterol")
plt.figure(figsize=(16, 8))
plt.hist(data_df["gluc"])
plt.title("gluc")
plt.figure(figsize=(16, 8))
plt.hist(data_df["smoke"])
plt.title("smoke")
plt.figure(figsize=(16, 8))
plt.hist(data_df["alco"])
plt.title("alco")
plt.figure(figsize=(16, 8))
plt.hist(data_df["active"])
plt.title("active")
plt.figure(figsize=(16, 8))
plt.hist(data_df["cardio"])
plt.title("cardio")
plt.show()

y = data_df["cardio"]
x = data_df.drop('cardio', axis = 1)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.25)

pca = PCA(n_components=11)
X_train = pca.fit_transform(x_train)
X_test = pca.fit_transform(x_test)
print(X_train.shape)

"""
scaler = preprocessing.StandardScaler().fit(x_train)
X_train = scaler.transform(x_train)
X_test = x_test
#"""

def save(filename,model):
    pickle.dump(model, open(filename, 'wb'))
    
start = time.time()
logreg = LogisticRegression(max_iter=1000)
logreg.fit(X_train, y_train)
y_pred = logreg.predict(X_test)
acc_log = logreg.score(X_train, y_train)
print("LR Train Accuracy:",acc_log)
print("LR Test Accuracy:",metrics.accuracy_score(y_test, y_pred))
print(metrics.classification_report(y_test, y_pred))
save("LR_model.sav",logreg)
print(time.time()-start)

start = time.time()
decision_tree = DecisionTreeClassifier(criterion="entropy", max_depth=3)
decision_tree = decision_tree.fit(X_train, y_train)
y_pred  = decision_tree.predict(X_test)
acc_decision_tree = decision_tree.score(X_train, y_train)
print("DT Train Accuracy:",acc_decision_tree)
print("DT Test Accuracy:",metrics.accuracy_score(y_test, y_pred))
print(metrics.classification_report(y_test, y_pred))
save("DT_model.sav",decision_tree)
print(time.time()-start)

start = time.time()
SVM = SVC(kernel='linear', probability=True)
SVM = SVM.fit(X_train, y_train)
y_pred  = SVM.predict(X_test)
acc_SVM = SVM.score(X_train, y_train)
print("SVM Train Accuracy:",acc_SVM)
print("SVM Test Accuracy:",metrics.accuracy_score(y_test, y_pred))
print(metrics.classification_report(y_test, y_pred))
save("SVM_model.sav",SVM)
print(time.time()-start)

start = time.time()
rf = RandomForestRegressor(n_estimators = 500)
rf.fit(X_train, y_train);
y_preds = rf.predict(X_test)
y_pred = []
for i in y_preds:
    if i < 0.5:
        y_pred.append(0)
    else:
        y_pred.append(1)
acc_RF = rf.score(X_train, y_train)
print("RF Train Accuracy:",acc_RF)
print("RF Test Accuracy:",metrics.accuracy_score(y_test, y_pred))
print(metrics.classification_report(y_test, y_pred))
save("RF_model.sav",rf)
print(time.time()-start)

