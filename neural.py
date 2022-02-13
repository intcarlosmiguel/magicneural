import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.cluster import KMeans
from keras.models import Sequential
from keras.layers import Dense,Dropout
from keras.utils import np_utils

def readFile(path):
    obj = cv2.imread("img/"+path)
    obj2 = np.copy(obj)
    obj2.T[0] = obj.T[2]
    obj2.T[2] = obj.T[0]
    obj = np.copy(obj2)
    #plt.figure(figsize=(8, 6), dpi=80)
    #plt.imshow(obj)
    plt.show()
    return obj

def GenerateColor():
    colors = []
    color = []
    color.append('Black')
    color.append('Blue')
    color.append('green')
    color.append('Red')
    color.append('White')
    for i in color:
        for j in range(300):
            colors.append([i+str(j),i])
    colors = np.array(colors)
    path = "C://Users//Blade//Downloads//Carlos Miguel//Python//K-means//img"
    dir_list = os.listdir(path)
    color = []
    for i in range(len(dir_list)):
        color.append([dir_list[i],colors.T[1][i]])
    color = np.array(color)
    return color

def calc(obj):
    return np.mean(np.mean(obj,axis = 0),axis = 0)

def selectData(dados,p):
    L = dados.shape[0]
    teste = np.random.choice(2, L, p=[p, 1-p])
    treino = dados[teste==0]
    teste = dados[teste==1]
    return treino,teste

def GenerateData():
    result = np.array([1,2,3])
    color = GenerateColor()
    for i in color:
        obj = readFile(i[0])[27:-27,27:-27]
        result = np.vstack([result, calc(obj)])
    result = result[1:]
    cores = color.T[1]
    hist = []
    for cor in cores:
        if(cor not in hist):
            hist.append(cor)
    hist = np.array(hist)
    for i in range(len(hist)):
        cores[cores==hist[i]] = i
    cor = cores.reshape(-1,1)
    dados = np.hstack((result,cor)).astype(float)
    return dados

def Kmeans(x,n,q):
    np.random.seed(453)
    center = np.random.randint(2, size=(n, 3))
    print(center)
    for j in range(q):
        distance = []
        for i in range(len(center)):
            d1 = x-center[i]
            distance.append(np.sum(d1*d1,axis = 1))
        distance = np.sqrt(np.array(distance)).T
        minimo = np.argmin(distance, axis=1)
        distance = []
        for i in range(len(center)):
            distance.append((x[minimo==i,:].sum(axis=0)+center[i])/(len(x[minimo==i,:]) + 1))
        distance = np.array(distance)
        center = np.copy(distance)
    j = 0
    return center

def Normalize(X):
    media = np.mean(X.T,axis = 1)
    std =  np.std(X.T,axis = 1)
    X = (X-media)/std
    return X

def RedesNeurais(X,Y,X_,Y_):
    modelo = Sequential()
    modelo.add(Dense(units=60,input_dim = 3))
    modelo.add(Dense(units=60))
    modelo.add(Dense(units=40))
    modelo.add(Dense(units=5,activation = 'softmax'))
    modelo.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
    modelo.fit(X,Y,epochs=1000,validation_data=(X_,Y_))
    previsoes = modelo.predict(X_)
    return previsoes

dados = GenerateData()

treino,teste = selectData(dados,0.8)

X = treino[:,:3]
Y = treino[:,3:]
X_ = teste[:,:3]
Y_ = teste[:,3:]
Y = Y.T[0]
Y = np_utils.to_categorical(Y)
Y_ = Y_.T[0]
Y_ = np_utils.to_categorical(Y_)

previsoes = RedesNeurais(X,Y,X_,Y_)