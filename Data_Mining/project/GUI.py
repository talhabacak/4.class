# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 13:21:53 2022

@author: talha
"""

from PyQt5.QtGui import  QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import QPushButton, QComboBox, QSizePolicy, QApplication, QWidget, QLabel, QSpinBox
import sys
import pickle
from sklearn.decomposition import PCA
import pandas as pd

class Ui_Form(object):
    def setupUi(self, Form):
        self.imagePath = "image/cardio1-3.jpg"
        self.iconPath = "image/cardio2-3.jpg"
        self.initForm(Form)        
        self.initWidget()
        self.initClicked()
        self.loadModel()    
        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Cardiovascular Diseases - Analysis"))
        self.pushButton_run.setText(_translate("Form", "Predict"))
        
    def initForm(self,Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(720, 360)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QSize(720, 360))
        Form.setMinimumSize(QSize(720, 360))
        #Form.setMaximumSize(QSize(1024, 768))
        Form.setSizeIncrement(QSize(1, 1))
        Form.setBaseSize(QSize(720, 360))
        Form.setMouseTracking(True)
        Form.setWindowIcon(QIcon(self.iconPath))
        Form.setStyleSheet("color: rgb(255, 255, 255);\n"
"selection-color: rgb(255, 85, 255);\n"
"background-color: rgb(255,127,36);\n"
"")
        
    def initWidget(self):
        self.label_resultMain = QLabel(Form)
        self.label_resultMain.setMouseTracking(True)
        self.label_resultMain.setLayoutDirection(Qt.LeftToRight)
        self.label_resultMain.setAutoFillBackground(False)
        self.label_resultMain.setStyleSheet("font: 11pt; color: rgb(255, 255, 255); background-color: rgb(2,9,18)")
        self.label_resultMain.setInputMethodHints(Qt.ImhHiddenText)
        self.label_resultMain.setAlignment(Qt.AlignLeft)
        self.label_resultMain.setWordWrap(False)
        self.label_resultMain.setObjectName("label_resultMain")
        self.label_resultMain.setGeometry(580,0,495,360)
        
        self.label_image = QLabel(Form)
        self.label_image.setMouseTracking(True)
        self.label_image.setLayoutDirection(Qt.LeftToRight)
        self.label_image.setAutoFillBackground(False)
        self.label_image.setStyleSheet("font: 11pt; color: rgb(2, 9, 18); background-color: rgb(65,65,65)")
        self.label_image.setInputMethodHints(Qt.ImhHiddenText)
        self.label_image.setAlignment(Qt.AlignLeft)
        self.label_image.setWordWrap(False)
        self.label_image.setObjectName("label_image")
        self.label_image.setGeometry(105,5,470,350)
        
        self.label_button = QLabel(Form)
        self.label_button.setMouseTracking(True)
        self.label_button.setLayoutDirection(Qt.LeftToRight)
        self.label_button.setAutoFillBackground(False)
        self.label_button.setStyleSheet("font: 11pt; color: rgb(2, 9, 18); background-color: rgb(2,9,18)")
        self.label_button.setInputMethodHints(Qt.ImhHiddenText)
        self.label_button.setAlignment(Qt.AlignLeft)
        self.label_button.setWordWrap(False)
        self.label_button.setObjectName("label_button")
        self.label_button.setGeometry(0,0,100,360)
                
        self.pushButton_run = QPushButton(Form)
        self.pushButton_run.setStyleSheet("font: 11pt; color: rgb(255, 255, 255);\n"
"background-color: rgb(255,127,36); font-weight: bold; border-radius : 50; border : 2px solid #F5F5F5")
        self.pushButton_run.setObjectName("pushButton_run")
        self.pushButton_run.setGeometry(10,80,80,30)
        
        self.label_model = QLabel(self.label_button)
        self.label_model.setMouseTracking(True)
        self.label_model.setLayoutDirection(Qt.LeftToRight)
        self.label_model.setAutoFillBackground(False)
        self.label_model.setStyleSheet("font: 11pt; color: rgb(238, 255, 221); font-weight: bold;")
        self.label_model.setInputMethodHints(Qt.ImhHiddenText)
        self.label_model.setAlignment(Qt.AlignCenter)
        self.label_model.setWordWrap(False)
        self.label_model.setObjectName("label_model")
        self.label_model.setGeometry(10, 10, 80, 30)
        self.label_model.setText("Model")
        
        self.comboBox_model = QComboBox(Form)
        self.comboBox_model.setStyleSheet("font: 11pt; background-color: rgb(238, 255, 221);\n"
"selection-color: rgb(0,0,0); selection-background-color: rgb(218, 235, 201); color: rgb(0,0,0)")
        self.comboBox_model.setObjectName("comboBox_model")
        self.comboBox_model.setGeometry(10,40,80,30)
        self.comboBox_model.addItem("LR")
        self.comboBox_model.addItem("DT")
        self.comboBox_model.addItem("RF")
        self.comboBox_model.addItem("SVM")
        
        self.label_age = QLabel(self.label_image)
        self.label_age.setMouseTracking(True)
        self.label_age.setLayoutDirection(Qt.LeftToRight)
        self.label_age.setAutoFillBackground(False)
        self.label_age.setStyleSheet("font: 10pt; color: rgb(255, 255, 255); font-weight: bold;")
        self.label_age.setInputMethodHints(Qt.ImhHiddenText)
        self.label_age.setAlignment(Qt.AlignCenter)
        self.label_age.setWordWrap(False)
        self.label_age.setObjectName("label_age")
        self.label_age.setGeometry(10, 10, 105, 30)
        self.label_age.setText("Age")
        
        self.spinBox_age = QSpinBox(self.label_image)
        self.spinBox_age.setGeometry(10, 40, 105, 30)
        self.spinBox_age.setMinimum(15)
        self.spinBox_age.setMaximum(150)
        self.spinBox_age.setProperty("value", 45)
        self.spinBox_age.setAlignment(Qt.AlignCenter)
        self.spinBox_age.setStyleSheet("font: 11pt; color: rgb(65, 65, 65);selection-color: rgb(0,0,0); selection-background-color: rgb(218, 235, 201);\n"
"background-color: rgb(255,127,36); font-weight: bold; border-radius : 50; border : 2px solid #F5F5F5")
        self.spinBox_age.setObjectName("spinBox_age")
    
        self.label_height = QLabel(self.label_image)
        self.label_height.setMouseTracking(True)
        self.label_height.setLayoutDirection(Qt.LeftToRight)
        self.label_height.setAutoFillBackground(False)
        self.label_height.setStyleSheet("font: 10pt; color: rgb(255, 255, 255); font-weight: bold;")
        self.label_height.setInputMethodHints(Qt.ImhHiddenText)
        self.label_height.setAlignment(Qt.AlignCenter)
        self.label_height.setWordWrap(False)
        self.label_height.setObjectName("label_height")
        self.label_height.setGeometry(125, 10, 105, 30)
        self.label_height.setText("Height (cm)")
        
        self.spinBox_height = QSpinBox(self.label_image)
        self.spinBox_height.setGeometry(125, 40, 105, 30)
        self.spinBox_height.setMinimum(100)
        self.spinBox_height.setMaximum(250)
        self.spinBox_height.setAlignment(Qt.AlignCenter)
        self.spinBox_height.setProperty("value", 170)
        self.spinBox_height.setStyleSheet("font: 11pt; color: rgb(65, 65, 65);selection-color: rgb(0,0,0); selection-background-color: rgb(218, 235, 201);\n"
"background-color: rgb(255,127,36); font-weight: bold; border-radius : 50; border : 2px solid #F5F5F5")
        self.spinBox_height.setObjectName("spinBox_height")
        
        self.label_weight = QLabel(self.label_image)
        self.label_weight.setMouseTracking(True)
        self.label_weight.setLayoutDirection(Qt.LeftToRight)
        self.label_weight.setAutoFillBackground(False)
        self.label_weight.setStyleSheet("font: 10pt; color: rgb(255, 255, 255); font-weight: bold;")
        self.label_weight.setInputMethodHints(Qt.ImhHiddenText)
        self.label_weight.setAlignment(Qt.AlignCenter)
        self.label_weight.setWordWrap(False)
        self.label_weight.setObjectName("label_weight")
        self.label_weight.setGeometry(240, 10, 105, 30)
        self.label_weight.setText("Weight (kg)")
        
        self.spinBox_weight = QSpinBox(self.label_image)
        self.spinBox_weight.setGeometry(240, 40, 105, 30)
        self.spinBox_weight.setMinimum(25)
        self.spinBox_weight.setMaximum(350)
        self.spinBox_weight.setAlignment(Qt.AlignCenter)
        self.spinBox_weight.setProperty("value", 70)
        self.spinBox_weight.setStyleSheet("font: 11pt; color: rgb(65, 65, 65);selection-color: rgb(0,0,0); selection-background-color: rgb(218, 235, 201);\n"
"background-color: rgb(255,127,36); font-weight: bold; border-radius : 50; border : 2px solid #F5F5F5")
        self.spinBox_weight.setObjectName("spinBox_weight")
        
        self.label_gender = QLabel(self.label_image)
        self.label_gender.setMouseTracking(True)
        self.label_gender.setLayoutDirection(Qt.LeftToRight)
        self.label_gender.setAutoFillBackground(False)
        self.label_gender.setStyleSheet("font: 10pt; color: rgb(255, 255, 255); font-weight: bold;")
        self.label_gender.setInputMethodHints(Qt.ImhHiddenText)
        self.label_gender.setAlignment(Qt.AlignCenter)
        self.label_gender.setWordWrap(False)
        self.label_gender.setObjectName("label_gender")
        self.label_gender.setGeometry(355, 10, 105, 30)
        self.label_gender.setText("Gender")
        
        self.comboBox_gender = QComboBox(self.label_image)
        self.comboBox_gender.setStyleSheet("font: 11pt; color: rgb(65, 65, 65);selection-color: rgb(0,0,0); selection-background-color: rgb(218, 235, 201);\n"
"background-color: rgb(255,127,36); font-weight: bold; border-radius : 50; border : 2px solid #F5F5F5")
        self.comboBox_gender.setObjectName("comboBox_gender")
        self.comboBox_gender.setEditable(True)
        self.comboBox_gender.lineEdit().setAlignment(Qt.AlignCenter)
        self.comboBox_gender.setGeometry(355, 40, 105, 30)
        self.comboBox_gender.addItem("Female")
        self.comboBox_gender.addItem("Male")
        
        self.label_smoke = QLabel(self.label_image)
        self.label_smoke.setMouseTracking(True)
        self.label_smoke.setLayoutDirection(Qt.LeftToRight)
        self.label_smoke.setAutoFillBackground(False)
        self.label_smoke.setStyleSheet("font: 10pt; color: rgb(255, 255, 255); font-weight: bold;")
        self.label_smoke.setInputMethodHints(Qt.ImhHiddenText)
        self.label_smoke.setAlignment(Qt.AlignCenter)
        self.label_smoke.setWordWrap(False)
        self.label_smoke.setObjectName("label_smoke")
        self.label_smoke.setGeometry(10, 90, 145, 30)
        self.label_smoke.setText("Smoke")
        
        self.comboBox_smoke = QComboBox(self.label_image)
        self.comboBox_smoke.setStyleSheet("font: 11pt; color: rgb(65, 65, 65);selection-color: rgb(0,0,0); selection-background-color: rgb(218, 235, 201);\n"
"background-color: rgb(255,127,36); font-weight: bold; border-radius : 50; border : 2px solid #F5F5F5")
        self.comboBox_smoke.setObjectName("comboBox_smoke")
        self.comboBox_smoke.setGeometry(10, 120, 145, 30)
        self.comboBox_smoke.setEditable(True)
        self.comboBox_smoke.lineEdit().setAlignment(Qt.AlignCenter)
        self.comboBox_smoke.addItem("No")
        self.comboBox_smoke.addItem("Yes")
        
        self.label_alcohol = QLabel(self.label_image)
        self.label_alcohol.setMouseTracking(True)
        self.label_alcohol.setLayoutDirection(Qt.LeftToRight)
        self.label_alcohol.setAutoFillBackground(False)
        self.label_alcohol.setStyleSheet("font: 10pt; color: rgb(255, 255, 255); font-weight: bold;")
        self.label_alcohol.setInputMethodHints(Qt.ImhHiddenText)
        self.label_alcohol.setAlignment(Qt.AlignCenter)
        self.label_alcohol.setWordWrap(False)
        self.label_alcohol.setObjectName("label_alcohol")
        self.label_alcohol.setGeometry(165, 90, 140, 30)
        self.label_alcohol.setText("Alcohol")
        
        self.comboBox_alcohol = QComboBox(self.label_image)
        self.comboBox_alcohol.setStyleSheet("font: 11pt; color: rgb(65, 65, 65);selection-color: rgb(0,0,0); selection-background-color: rgb(218, 235, 201);\n"
"background-color: rgb(255,127,36); font-weight: bold; border-radius : 50; border : 2px solid #F5F5F5")
        self.comboBox_alcohol.setObjectName("comboBox_alcohol")
        self.comboBox_alcohol.setGeometry(165, 120, 140, 30)
        self.comboBox_alcohol.setEditable(True)
        self.comboBox_alcohol.lineEdit().setAlignment(Qt.AlignCenter)
        self.comboBox_alcohol.addItem("No")
        self.comboBox_alcohol.addItem("Yes")
        
        self.label_activity = QLabel(self.label_image)
        self.label_activity.setMouseTracking(True)
        self.label_activity.setLayoutDirection(Qt.LeftToRight)
        self.label_activity.setAutoFillBackground(False)
        self.label_activity.setStyleSheet("font: 10pt; color: rgb(255, 255, 255); font-weight: bold;")
        self.label_activity.setInputMethodHints(Qt.ImhHiddenText)
        self.label_activity.setAlignment(Qt.AlignCenter)
        self.label_activity.setWordWrap(False)
        self.label_activity.setObjectName("label_activity")
        self.label_activity.setGeometry(315, 90, 145, 30)
        self.label_activity.setText("P. Activity")
        
        self.comboBox_activity = QComboBox(self.label_image)
        self.comboBox_activity.setStyleSheet("font: 11pt; color: rgb(65, 65, 65);selection-color: rgb(0,0,0); selection-background-color: rgb(218, 235, 201);\n"
"background-color: rgb(255,127,36); font-weight: bold; border-radius : 50; border : 2px solid #F5F5F5")
        self.comboBox_activity.setObjectName("comboBox_activity")
        self.comboBox_activity.setGeometry(315, 120, 145, 30)
        self.comboBox_activity.setEditable(True)
        self.comboBox_activity.lineEdit().setAlignment(Qt.AlignCenter)
        self.comboBox_activity.addItem("No")
        self.comboBox_activity.addItem("Yes")
        
        self.label_low = QLabel(self.label_image)
        self.label_low.setMouseTracking(True)
        self.label_low.setLayoutDirection(Qt.LeftToRight)
        self.label_low.setAutoFillBackground(False)
        self.label_low.setStyleSheet("font: 10pt; color: rgb(255, 255, 255); font-weight: bold;")
        self.label_low.setInputMethodHints(Qt.ImhHiddenText)
        self.label_low.setAlignment(Qt.AlignCenter)
        self.label_low.setWordWrap(False)
        self.label_low.setObjectName("label_low")
        self.label_low.setGeometry(10, 170, 220, 30)
        self.label_low.setText("Diastolic blood pressure")
        
        self.spinBox_low = QSpinBox(self.label_image)
        self.spinBox_low.setGeometry(10, 200, 220, 30)
        self.spinBox_low.setMinimum(1)
        self.spinBox_low.setMaximum(300)
        self.spinBox_low.setAlignment(Qt.AlignCenter)
        self.spinBox_low.setProperty("value", 80)
        self.spinBox_low.setStyleSheet("font: 11pt; color: rgb(65, 65, 65);selection-color: rgb(0,0,0); selection-background-color: rgb(218, 235, 201);\n"
"background-color: rgb(255,127,36); font-weight: bold; border-radius : 50; border : 2px solid #F5F5F5")
        self.spinBox_low.setObjectName("spinBox_low")
        
        self.label_high = QLabel(self.label_image)
        self.label_high.setMouseTracking(True)
        self.label_high.setLayoutDirection(Qt.LeftToRight)
        self.label_high.setAutoFillBackground(False)
        self.label_high.setStyleSheet("font: 10pt; color: rgb(255, 255, 255); font-weight: bold;")
        self.label_high.setInputMethodHints(Qt.ImhHiddenText)
        self.label_high.setAlignment(Qt.AlignCenter)
        self.label_high.setWordWrap(False)
        self.label_high.setObjectName("label_high")
        self.label_high.setGeometry(240, 170, 220, 30)
        self.label_high.setText("Systolic blood pressure")
        
        self.spinBox_high = QSpinBox(self.label_image)
        self.spinBox_high.setGeometry(240, 200, 220, 30)
        self.spinBox_high.setMinimum(1)
        self.spinBox_high.setMaximum(400)
        self.spinBox_high.setAlignment(Qt.AlignCenter)
        self.spinBox_high.setProperty("value", 120)
        self.spinBox_high.setStyleSheet("font: 11pt; color: rgb(65, 65, 65);selection-color: rgb(0,0,0); selection-background-color: rgb(218, 235, 201);\n"
"background-color: rgb(255,127,36); font-weight: bold; border-radius : 50; border : 2px solid #F5F5F5")
        self.spinBox_high.setObjectName("spinBox_high")
        
        self.label_cholesterol = QLabel(self.label_image)
        self.label_cholesterol.setMouseTracking(True)
        self.label_cholesterol.setLayoutDirection(Qt.LeftToRight)
        self.label_cholesterol.setAutoFillBackground(False)
        self.label_cholesterol.setStyleSheet("font: 10pt; color: rgb(255, 255, 255); font-weight: bold;")
        self.label_cholesterol.setInputMethodHints(Qt.ImhHiddenText)
        self.label_cholesterol.setAlignment(Qt.AlignCenter)
        self.label_cholesterol.setWordWrap(False)
        self.label_cholesterol.setObjectName("label_cholesterol")
        self.label_cholesterol.setGeometry(10, 250, 220, 30)
        self.label_cholesterol.setText("Cholesterol ")
        
        self.comboBox_cholesterol = QComboBox(self.label_image)
        self.comboBox_cholesterol.setStyleSheet("font: 11pt; color: rgb(65, 65, 65);selection-color: rgb(0,0,0); selection-background-color: rgb(218, 235, 201);\n"
"background-color: rgb(255,127,36); font-weight: bold; border-radius : 50; border : 2px solid #F5F5F5")
        self.comboBox_cholesterol.setObjectName("comboBox_cholesterol")
        self.comboBox_cholesterol.setGeometry(10, 280, 220, 30)
        self.comboBox_cholesterol.setEditable(True)
        self.comboBox_cholesterol.lineEdit().setAlignment(Qt.AlignCenter)
        self.comboBox_cholesterol.addItem("Normal")
        self.comboBox_cholesterol.addItem("Above Normal")
        self.comboBox_cholesterol.addItem("Well Above Normal")
        
        self.label_glucose = QLabel(self.label_image)
        self.label_glucose.setMouseTracking(True)
        self.label_glucose.setLayoutDirection(Qt.LeftToRight)
        self.label_glucose.setAutoFillBackground(False)
        self.label_glucose.setStyleSheet("font: 10pt; color: rgb(255, 255, 255); font-weight: bold;")
        self.label_glucose.setInputMethodHints(Qt.ImhHiddenText)
        self.label_glucose.setAlignment(Qt.AlignCenter)
        self.label_glucose.setWordWrap(False)
        self.label_glucose.setObjectName("label_glucose")
        self.label_glucose.setGeometry(240, 250, 220, 30)
        self.label_glucose.setText("Glucose  ")
        
        self.comboBox_glucose = QComboBox(self.label_image)
        self.comboBox_glucose.setStyleSheet("font: 11pt; color: rgb(65, 65, 65);selection-color: rgb(0,0,0); selection-background-color: rgb(218, 235, 201);\n"
"background-color: rgb(255,127,36); font-weight: bold; border-radius : 50; border : 2px solid #F5F5F5")
        self.comboBox_glucose.setObjectName("comboBox_glucose")
        self.comboBox_glucose.setGeometry(240, 280, 220, 30)
        self.comboBox_glucose.setEditable(True)
        self.comboBox_glucose.lineEdit().setAlignment(Qt.AlignCenter)
        self.comboBox_glucose.addItem("Normal")
        self.comboBox_glucose.addItem("Above Normal")
        self.comboBox_glucose.addItem("Well Above Normal")
        
        self.label_result = QLabel(self.label_resultMain)
        self.label_result.setMouseTracking(True)
        self.label_result.setLayoutDirection(Qt.LeftToRight)
        self.label_result.setAutoFillBackground(False)
        self.label_result.setStyleSheet("font: 12pt; color: rgb(255,127,36); font-weight: bold;")
        self.label_result.setInputMethodHints(Qt.ImhHiddenText)
        self.label_result.setAlignment(Qt.AlignCenter)
        self.label_result.setWordWrap(False)
        self.label_result.setObjectName("label_result")
        self.label_result.setGeometry(10, 10, 120, 30)
        self.label_result.setText("RESULT")
        
        self.label_disease = QLabel(self.label_resultMain)
        self.label_disease.setMouseTracking(True)
        self.label_disease.setLayoutDirection(Qt.LeftToRight)
        self.label_disease.setAutoFillBackground(False)
        self.label_disease.setStyleSheet("font: 9pt; color: rgb(255, 255, 255); font-weight: bold;")
        self.label_disease.setInputMethodHints(Qt.ImhHiddenText)
        self.label_disease.setAlignment(Qt.AlignCenter)
        self.label_disease.setWordWrap(False)
        self.label_disease.setObjectName("label_disease")
        self.label_disease.setGeometry(10, 50, 120, 90)
        self.label_disease.setText("Presence\nof\ncardiovascular\ndisease:")
        
        self.label_disease_presence = QLabel(self.label_resultMain)
        self.label_disease_presence.setMouseTracking(True)
        self.label_disease_presence.setLayoutDirection(Qt.LeftToRight)
        self.label_disease_presence.setAutoFillBackground(False)
        self.label_disease_presence.setStyleSheet("font: 11pt; color: rgb(255, 255, 255); font-weight: bold;")
        self.label_disease_presence.setInputMethodHints(Qt.ImhHiddenText)
        self.label_disease_presence.setAlignment(Qt.AlignCenter)
        self.label_disease_presence.setWordWrap(False)
        self.label_disease_presence.setObjectName("label_disease_presence")
        self.label_disease_presence.setGeometry(10, 150,120, 30)
        
        self.label_disease_2 = QLabel(self.label_resultMain)
        self.label_disease_2.setMouseTracking(True)
        self.label_disease_2.setLayoutDirection(Qt.LeftToRight)
        self.label_disease_2.setAutoFillBackground(False)
        self.label_disease_2.setStyleSheet("font: 9pt; color: rgb(255, 255, 255); font-weight: bold;")
        self.label_disease_2.setInputMethodHints(Qt.ImhHiddenText)
        self.label_disease_2.setAlignment(Qt.AlignCenter)
        self.label_disease_2.setWordWrap(False)
        self.label_disease_2.setObjectName("label_disease_2")
        self.label_disease_2.setGeometry(10, 190,120, 20)
        self.label_disease_2.setText("Probability:")
        
        self.label_disease_prob = QLabel(self.label_resultMain)
        self.label_disease_prob.setMouseTracking(True)
        self.label_disease_prob.setLayoutDirection(Qt.LeftToRight)
        self.label_disease_prob.setAutoFillBackground(False)
        self.label_disease_prob.setStyleSheet("font: 11pt; color: rgb(255, 255, 255); font-weight: bold;")
        self.label_disease_prob.setInputMethodHints(Qt.ImhHiddenText)
        self.label_disease_prob.setAlignment(Qt.AlignCenter)
        self.label_disease_prob.setWordWrap(False)
        self.label_disease_prob.setObjectName("label_disease_prob")
        self.label_disease_prob.setGeometry(10, 220,120, 30)
        
        self.label_image2 = QLabel(self.label_resultMain)
        self.label_image2.setMouseTracking(True)
        self.label_image2.setLayoutDirection(Qt.LeftToRight)
        self.label_image2.setAutoFillBackground(False)
        self.label_image2.setStyleSheet("font: 11pt; color: rgb(255, 255, 255); font-weight: bold;")
        self.label_image2.setInputMethodHints(Qt.ImhHiddenText)
        self.label_image2.setAlignment(Qt.AlignCenter)
        self.label_image2.setWordWrap(False)
        self.label_image2.setObjectName("label_image2")
        self.label_image2.setGeometry(5, 250,130, 105)
        self.pixmap = QPixmap(self.imagePath)
        self.label_image2.setPixmap(self.pixmap)
        # self.label_image2.resize(self.pixmap.width(),self.pixmap.height())
        
    def initClicked(self):
        self.pushButton_run.clicked.connect(self.run)
        
    def predict(self,data):
        pathData = r'data/cardioTrain_2.csv'
        useCols = ["age","gender","height","weight","ap_hi","ap_lo","cholesterol","gluc","smoke","alco","active","cardio"]
        data_df = pd.read_csv(pathData,on_bad_lines='skip',usecols=useCols)
        data_df["gender"] = data_df["gender"] - 1
        x = data_df.drop('cardio', axis = 1)
        x.loc[x.shape[0]] = data
        pca = PCA(n_components=11)
        X = pca.fit_transform(x)
        target = X[-1:]
        if self.comboBox_model.currentIndex() == 0:
            pred_y = self.model_LR.predict(target)
            pred_proba = self.model_LR.predict_proba(target)
        elif self.comboBox_model.currentIndex() == 1:
            pred_y = self.model_DT.predict(target)
            pred_proba = self.model_DT.predict_proba(target)
        elif self.comboBox_model.currentIndex() == 2:
            pred_y = self.model_DT.predict(target)
            pred_proba = self.model_DT.predict_proba(target)
        elif self.comboBox_model.currentIndex() == 3:
            pred_y = self.model_SVM.predict(target)
            pred_proba = self.model_SVM.predict_proba(target)
        
        if pred_y == 1:
            self.label_disease_presence.setText("Yes")
            self.label_disease_presence.setStyleSheet("color: rgb(255,0,0)")
            self.label_disease_prob.setText("% " + str(int(pred_proba[0][1]*100)))
            self.label_disease_prob.setStyleSheet("color: rgb(255,0,0)")
        else:
            self.label_disease_presence.setText("No")
            self.label_disease_presence.setStyleSheet("color: rgb(0,255,0)")
            self.label_disease_prob.setText("% " + str(int(pred_proba[0][1]*100)))
            self.label_disease_prob.setStyleSheet("color: rgb(0,255,0)")
    
    def loadModel(self):
        self.model_LR = pickle.load(open("model/LR_model.sav", 'rb'))
        self.model_DT = pickle.load(open("model/DT_model.sav", 'rb'))
        self.model_RF = pickle.load(open("model/RF_model.sav", 'rb'))
        self.model_SVM = pickle.load(open("model/SVM_model.sav", 'rb'))
    
    def run(self,x):
        self.age = int(self.spinBox_age.value())
        self.height = int(self.spinBox_height.value())
        self.weight = int(self.spinBox_weight.value())
        self.low = int(self.spinBox_low.value())
        self.high = int(self.spinBox_high.value())
        self.gender = int(self.comboBox_gender.currentIndex())
        self.cholesterol = int(self.comboBox_cholesterol.currentIndex()) + 1
        self.glucose = int(self.comboBox_glucose.currentIndex()) + 1
        self.smoke = int(self.comboBox_smoke.currentIndex())
        self.alcohol = int(self.comboBox_alcohol.currentIndex())
        self.activity = int(self.comboBox_activity.currentIndex())

        x = [self.age,self.gender,self.height,self.weight,self.high,self.low,self.cholesterol,self.glucose,self.smoke,self.alcohol,self.activity]
        self.predict(x)

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    Form = QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
    