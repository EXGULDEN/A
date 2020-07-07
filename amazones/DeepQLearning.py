from NeuralNetwork import NeuralNetwork
from ExperienceReplay import ExperienceReplay
from numpy import *
import random


class DeepQLearning(object):
    
    def __init__(self):
        self.targetNN=NeuralNetwork()
        self.mainNN=NeuralNetwork()
        self.exp=ExperienceReplay(10000)
        self.batch_size=32
        self.Epsilon=0.9
        self.Lambda=0.9
        self.map,self.map_=self.makemap(10)

    def start(self):
        self.mainNN.Firstmodel()
        self.targetNN.Firstmodel()

    def load(self,name):
        self.targetNN.Loadmodel(name)
        self.mainNN.Loadmodel(name)

    def saveModel(self,name):
        self.targetNN.Savemodel(name)


    def getNext(self,situation,numlist,israndom):
        ran=(random.uniform(0,1)>self.Epsilon)
        if ran or israndom:
            rannum=random.sample(numlist,1)
            print(rannum[0][0],rannum[0][1],rannum[0][2],rannum[0][3])
            max_index=self.map_[rannum[0][0],rannum[0][1],rannum[0][2],rannum[0][3]]
        else:
            index=self.mainNN.model.predict(situation)
            max_index=index.argmax()
        return self.getMove(max_index)


    def getMove(self,index):
        num=int(index)
        if num<2940:
            z=self.map[num]
            return num,z[0],z[1],z[2],z[3]            
        elif num>=2940:
            z=-1
            numm=num-2940
            x=int(numm/10)
            y=numm%10
            return num,x,y,x,y
            

    def saveEXP(self,fistS,action,reward,done,nextS):
        self.exp.add(fistS,action,reward,done,nextS)
        
    def learn(self):
        if self.exp.tree.flag:
            return
        fistS,actrew,nextS,idxl,isweight=self.exp.getDate(self.batch_size)
        qtarget=[]
        for i in nextS:
            targetv=self.targetNN.model.predict(i)
            mainv=self.mainNN.model.predict(i)
            for tv,mv in zip(targetv,mainv):
                v=tv[argmax(mv)]
                qtarget.append(v)
        k=0
        ans=[]
        errors=empty(self.batch_size)
        for i,j,done in actrew:
            r=zeros(3040)
            r[i]+=j+(1-done)*self.Lambda*qtarget[k]
            ans.append(r)
            errors[k]=abs(mainv[0][i]-r[i])
            k+=1
        self.mainNN.Training(fistS,ans,isweight)
        self.exp.batch_updata(idxl,errors)

    def copy(self):
        self.targetNN.copy(self.mainNN.model.get_weights())

    def makemap(self,n):
        ans=[]
        for i in range(n):
            for j in range(n):
                for k in range(1,n):
                    if i<n and i>=0 and j+k<n and j+k>=0:
                        ans.append([i,j,i,j+k])
                for k in range(1,n):
                    if i+k<n and i+k>=0 and j+k<n and j+k>=0:
                        ans.append([i,j,i+k,j+k])
                for k in range(1,n):
                    if i+k<n and i+k>=0 and j<n and j>=0:
                        ans.append([i,j,i+k,j])
                for k in range(1,n):
                    if i+k<n and i+k>=0 and j-k<n and j-k>=0:
                        ans.append([i,j,i+k,j-k])
                for k in range(1,n):
                    if i<n and i>=0 and j-k<n and j-k>=0:
                        ans.append([i,j,i,j-k])
                for k in range(1,n):
                    if i-k<n and i-k>=0 and j-k<n and j-k>=0:
                        ans.append([i,j,i-k,j-k])
                for k in range(1,n):
                    if i-k<n and i-k>=0 and j<n and j>=0:
                        ans.append([i,j,i-k,j])
                for k in range(1,n):
                    if i-k<n and i-k>=0 and j+k<n and j+k>=0:
                        ans.append([i,j,i-k,j+k])
        ans_=dict()
        k=0
        for i in ans:
            ans_[i[0],i[1],i[2],i[3]]=k
            k+=1
        for i in range(n):
            for j in range(n):
                ans_[i,j,i,j]=k
                k+=1
        return ans,ans_






        
