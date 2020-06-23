from keras.models import Sequential,load_model
from keras.layers import Dense, Activation, Convolution2D, MaxPooling2D, Flatten
from keras import backend as K
import numpy as np


class NeuralNetwork(object):

    def __init__(self):
        self.model=Sequential()
        self.Lambda=0.9
        

    def Firstmodel(self):
        self.model.add(Dense(output_dim=32,input_dim=100))
        self.model.add(Dense(output_dim=72))
        self.model.add(Dense(output_dim=388))
        self.model.compile(loss='mean_squared_error',optimizer='sgd')

    def Training(self,xtrain,ytrain,isweight):
        x_train=np.reshape(xtrain,(32,-1))
        y_train=np.reshape(ytrain,(32,-1))
        self.model.fit(x_train,y_train,batch_size=32,sample_weight=isweight)

    def copy(self,weights):
        self.model.set_weights(weights)

    def Loadmodel(self,name):
        self.model=load_model(name)

    def Savemodel(self,name):
        self.model.save(name)

    


        
        
