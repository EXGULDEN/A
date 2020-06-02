from NeuralNetwork import NeuralNetwork
from ExperienceReplay import ExperienceReplay
from numpy import *
import random


class DeepQLearning(object):
    
    def __init__(self):
        self.targetNN=NeuralNetwork()
        self.mainNN=NeuralNetwork()
        self.exp=ExperienceReplay(1000)
        self.batch_size=32
        self.Epsilon=0.9
        self.Lambda=0.9

    def start(self):
        self.mainNN.Firstmodel()
        self.targetNN.Firstmodel()

    def load(self,name):
        self.targetNN.Loadmodel(name)
        self.mainNN.Loadmodel(name)

    def saveModel(self,name):
        self.targetNN.Savemodel(name)


    def getNext(self,situation,numlist):
        ran=(random.uniform(0,1)<self.Epsilon)
        if ran:
            rannum=random.sample(numlist,1)
            max_index=rannum[0]
        else:
            index=self.mainNN.model.predict(situation)
            max_index=index.argmax()
        return self.getMove(max_index)


    def getMove(self,index):
        num=int(index)
        if num<288:
            z=int(num/72)
            numm=num-z*72
            xx=int(numm/9)
            yy=num%9
            if(xx==0):
                x=0
                y=1+yy
            elif(xx==1):
                x=1+yy
                y=1+yy
            elif(xx==2):
                x=1+yy
                y=0
            elif(xx==3):
                x=1+yy
                y=-1-yy
            elif(xx==4):
                x=0
                y=-1-yy
            elif(xx==5):
                x=-1-yy
                y=-1-yy
            elif(xx==6):
                x=-1-yy
                y=0
            elif(xx==7):
                x=-1-yy
                y=1+yy            
            return z,x,y,num
        elif num>=288:
            z=-1
            numm=num-288
            x=int(numm/10)
            y=numm%10
            return z,x,y,num
            

    def saveEXP(self,fistS,action,reward,done,nextS):
        self.exp.add(fistS,action,reward,done,nextS)
        
    def learn(self):
        size=self.exp.getSize()
        if(size<self.batch_size):
            return
        fistS,actrew,nextS=self.exp.getDate(self.batch_size)
        qtarget=[]
        for i in nextS:
            targetv=self.targetNN.model.predict(i)
            mainv=self.mainNN.model.predict(i)
            for tv,mv in zip(targetv,mainv):
                v=tv[argmax(mv)]
                qtarget.append(v)
        k=0
        ans=[]
        for i,j,done in actrew:
            r=zeros(388)
            r[i]+=j+(1-done)*self.Lambda*qtarget[k]
            ans.append(r)
            k+=1
        self.mainNN.Training(fistS,ans)

    def copy(self):
        self.targetNN.copy(self.mainNN.model.get_weights())






        
