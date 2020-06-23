import random as rand
from numpy import *
from SumTree import *


class ExperienceReplay(object):

    def __init__(self,size):
        self.size=size
        self.tree=SumTree(size)
        self.e=0.01
        self.alpha=0.6
        self.bata=0.4

    def add(self,fistS,action,reward,done,nextS):
        data=[]
        data=(fistS,action,reward,done,nextS)
        p=max(self.tree.tree[-self.tree.capacity:])
        if p==0:
            p=1
        self.tree.add(p,data)

        
    def getDate(self,n):
        fistS=[]
        actrew=[]
        nextS=[]
        isweight=empty(n)
        idxl=[]
        pri_seg=self.tree.total()/n
        min_p=min(self.tree.tree[-self.tree.capacity:])/self.tree.total()
        for i in range(n):
            l=pri_seg*i
            r=pri_seg*(i+1)
            v=rand.uniform(l,r)
            idx,p,data=self.tree.get(v)
            prob=p/self.tree.total()
            isweight[i]=prob
            idxl.append(idx)
            fistS.append(data[0].reshape(1,-1))
            actrew.append((data[1],data[2],data[3]))
            nextS.append(data[4].reshape(1,-1))
        return fistS,actrew,nextS,idxl,isweight

    def batch_updata(self,idx,errors):
        errors+=self.e
        p=power(errors,self.alpha)
        for i,j in zip(idx,p):
            self.tree.update(i,j)
    
    def getSize(self):
        return len(self.exp)
