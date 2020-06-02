
from keras.models import Sequential
from keras.layers.core import Activation, Dropout
from keras.layers.core import Dense
from keras.optimizers import SGD
 
from keras.datasets import mnist
from keras.utils import np_utils
 
 
import numpy as np
np.random.seed(1671)
 
 
#网络和训练
NB_EPOCH = 20
BATCH_SIZE = 128
VERBOSE = 1
NB_CLASSES = 10
OPTIMIZER = SGD()
N_HIDDEN = 128
VALIDATION_SPLIT = 0.2
DROPOUT = 0.3
 
 
#数据
(X_train, Y_train), (X_test, Y_test) = mnist.load_data()
 
RESHAPED = 784
 
X_train = X_train.reshape(60000, RESHAPED)
X_test = X_test.reshape(10000, RESHAPED)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
 
 
#归一化
X_train /= 255
X_test /= 255
 
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')
 
#将标签变成二进制类别矩阵
Y_train = np_utils.to_categorical(Y_train, NB_CLASSES)
Y_test = np_utils.to_categorical(Y_test, NB_CLASSES)
 
#模型的构建
model = Sequential()
model.add(Dense(N_HIDDEN, input_shape=(RESHAPED,)))
model.add(Activation('relu'))
model.add(Dropout(DROPOUT))
model.add(Dense(N_HIDDEN))
model.add(Activation('relu'))
model.add(Dense(NB_CLASSES))
model.add(Activation('softmax'))
model.summary()
 
#显示模型结构
print(model.summary())
 
#配置训练模型
model.compile(loss='categorical_crossentropy', optimizer=OPTIMIZER, metrics=['accuracy'])
#模型训练
history = model.fit(X_train, Y_train,
                    batch_size=BATCH_SIZE, epochs=NB_EPOCH,
                    verbose=VERBOSE, validation_split=VALIDATION_SPLIT)
 
#模型测试
score = model.evaluate(X_test, Y_test, verbose=VERBOSE)
print('test score:', score[0])
print('test accuracy:', score[1])
