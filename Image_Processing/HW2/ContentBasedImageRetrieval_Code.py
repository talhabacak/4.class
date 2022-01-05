# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 04:28:15 2021

@author: talha
"""

import cv2
import os 
import numpy as np
import math

class Resim:
    def __init__(self, name="", className="", R=[], G=[], B=[], H=[]):
        self.name = name
        self.className = className
        self.R = R
        self.G = G
        self.B = B
        self.H = H
        

def histRGBH(resim):
    hsvResim = cv2.cvtColor(resim, cv2.COLOR_BGR2HSV)
    yukseklik = resim.shape[0]
    genislik = resim.shape[1]
    boyut = genislik * yukseklik
    histR = np.zeros(256)
    histG = np.zeros(256)
    histB = np.zeros(256)
    histH = np.zeros(180)
    for i in range(yukseklik):
        for j in range(genislik):
            histB[resim.item(i,j,0)] += 1
            histG[resim.item(i,j,1)] += 1
            histR[resim.item(i,j,2)] += 1
            histH[hsvResim.item(i,j,0)] += 1         
    for i in range(histB.size):
        histB[i] = histB[i] / boyut
    for i in range(histG.size):
        histG[i] = histG[i] / boyut
    for i in range(histR.size):
        histR[i] = histR[i] / boyut
    for i in range(histH.size):
        histH[i] = histH[i] / boyut
    return histB, histG, histR, histH

def add(path, className):
    count=0
    for dosya in os.listdir(path):
        resim = cv2.imread(path+"/"+dosya)
        histB, histG, histR, histH = histRGBH(resim)
        if count < 20:
            resimTrain.append(Resim(dosya,className,histR,histG,histB,histH))
        elif count < 30:
            resimTest.append(Resim(dosya,className,histR,histG,histB,histH))
        else:
            break
        count += 1
        
def Euclidean(resim1, resim2):
    toplam = 0
    i = 0
    while i < resim1.size:
        toplam += (resim1.item(i) - resim2.item(i)) ** 2
        i += 1
    return math.sqrt(toplam)


resimTrain = []
resimTest = []


sinif = ["elephant","flamingo","kangaroo","Leopards","octopus","sea_horse"]

path_elephant = r"C:/Users/talha/Desktop/odev2/data/elephant"
path_flamingo = r"C:/Users/talha/Desktop/odev2/data/flamingo"
path_kangaroo = r"C:/Users/talha/Desktop/odev2/data/kangaroo"
path_Leopards = r"C:/Users/talha/Desktop/odev2/data/Leopards"
path_octopus = r"C:/Users/talha/Desktop/odev2/data/octopus"
path_sea_horse = r"C:/Users/talha/Desktop/odev2/data/sea_horse"

path_result = r"C:/Users/talha/Desktop/odev2/result.txt"

add(path_elephant, sinif[0])
add(path_flamingo, sinif[1])
add(path_kangaroo, sinif[2])
add(path_Leopards, sinif[3])
add(path_octopus, sinif[4])
add(path_sea_horse, sinif[5])

count = 0
accuarcyClassRGB = [0,0,0,0,0,0]
accuarcyGeneralRGB = 0
accuarcyClassHSV = [0,0,0,0,0,0]
accuarcyGeneralHSV = 0
data = ""

for i in resimTest:
    similarityRGB = [999999,999999,999999,999999,999999]
    similarityHSV = [999999,999999,999999,999999,999999]
    ResimRGB = [Resim(),Resim(),Resim(),Resim(),Resim()]
    RsimHSV = [Resim(),Resim(),Resim(),Resim(),Resim()]
    for j in resimTrain:
        similarityR = Euclidean(i.R,j.R)
        similarityG = Euclidean(i.G,j.G)
        similarityB = Euclidean(i.B,j.B)
        similarRGB = (similarityR + similarityG + similarityB) / 3
        similarHSV = Euclidean(i.H,j.H)
        
        if max(similarityRGB) > similarRGB:
            index = similarityRGB.index(max(similarityRGB))
            ResimRGB[index] = j
            similarityRGB[index] = similarRGB
        if max(similarityHSV) > similarHSV:
            index = similarityHSV.index(max(similarityHSV))
            RsimHSV[index] = j
            similarityHSV[index] = similarHSV
    
    print("Test Data:\tClass - "+i.className+"\tName - "+i.name)
    print("Best 5 Matches Train Data (RGB):")
    data += "Test Data:\tClass - "+i.className+"\tName - "+i.name +"\n"
    data += "Best 5 Matches Train Data (RGB):\n"
    flagRGB = 0
    flagHSV = 0
    for simRGB in ResimRGB:
        print("Class - "+simRGB.className+"\tName - "+simRGB.name)
        data += "Class - "+simRGB.className+"\tName - "+simRGB.name +"\n"
        if i.className == simRGB.className:
            flagRGB = 1
    print("Best 5 Matches Train Data (HSV):")
    data += "Best 5 Matches Train Data (HSV)\n:"
    for simHSV in RsimHSV:
        print("Class - "+simHSV.className+"\tName - "+simHSV.name)
        data += "Class - "+simHSV.className+"\tName - "+simHSV.name + "\n"
        if i.className == simHSV.className:
            flagHSV = 1
    if flagRGB == 1:
        accuarcyGeneralRGB += 1
        if count < 10:
            accuarcyClassRGB[0] += 1
        elif count < 20:
            accuarcyClassRGB[1] += 1
        elif count < 30:
            accuarcyClassRGB[2] += 1
        elif count < 40:
            accuarcyClassRGB[3] += 1
        elif count < 50:
            accuarcyClassRGB[4] += 1
        elif count < 60:
            accuarcyClassRGB[5] += 1
        else:
            print("Hata")
    if flagHSV == 1:
        accuarcyGeneralHSV += 1
        if count < 10:
            accuarcyClassHSV[0] += 1
        elif count < 20:
            accuarcyClassHSV[1] += 1
        elif count < 30:
            accuarcyClassHSV[2] += 1
        elif count < 40:
            accuarcyClassHSV[3] += 1
        elif count < 50:
            accuarcyClassHSV[4] += 1
        elif count < 60:
            accuarcyClassHSV[5] += 1
        else:
            print("Hata")
    count += 1

print("\nAccuarcy RGB")
print("General Accuarcy:" + str(accuarcyGeneralRGB / 60.00))
data += "\nAccuarcy RGB\n"
data += "General Accuarcy:" + str(accuarcyGeneralRGB / 60.00) + "\n"
for i in range(len(accuarcyClassRGB)):
    print(sinif[i]+":"+str(accuarcyClassRGB[i]/10.00))
    data += sinif[i]+":"+str(accuarcyClassRGB[i]/10.00) + "\n"
print("\nAccuarcy HSV")
print("General Accuarcy:" + str(accuarcyGeneralHSV / 60.00))
data += "\nAccuarcy HSV\n"
data += "General Accuarcy:" + str(accuarcyGeneralHSV / 60.00) + "\n"
for i in range(len(accuarcyClassHSV)):
    print(sinif[i]+":"+str(accuarcyClassHSV[i]/10.00))
    data += sinif[i]+":"+str(accuarcyClassHSV[i]/10.00) + "\n"

result = open(path_result,"w")
result.write(data)
result.close()

        