from keras.models import Sequential,load_model,Model
from keras.layers import Dense, Activation, Convolution2D, MaxPooling2D, Flatten,Input, Add, Subtract, Lambda
from keras import backend as K
import numpy as np


class NeuralNetwork(object):

    def __init__(self):
        self.model=Sequential()
        self.Lambda=0.9
        

    def Firstmodel(self):
        self.model.add(Dense(output_dim=100,input_dim=100))
        self.model.add(Dense(output_dim=10000))
        self.model.add(Dense(output_dim=3040))
        self.model.compile(loss='mean_squared_error',optimizer='sgd')

    def DuelingNetwork(self):
        inputs=Input(shape=(100,))
        x=Dense(320,activation='relu')(inputs)
        x=Dense(1000,activation='relu')(x)
        
        value=Dense(1,activation='linear')(x)
        a=Dense(3040,activation='linear')(x)
        meam = Lambda(lambda x: K.mean(x, axis=1, keepdims=True))(a)
        advantage = Subtract()([a, meam])
        q = Add()([value, advantage])
        self.model = Model(inputs=inputs, outputs=q)
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

    


        
        
