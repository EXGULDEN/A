import random as rand
from numpy import *



class ExperienceReplay(object):

    def __init__(self,size):
        self.size=size
        self.exp=[]

    def add(self,fistS,action,reward,done,nextS):
        self.exp.append(((fistS,action,reward,done,nextS)))
        if len(self.exp)>self.size:
            self.exp.pop(0)

    def getDate(self,n):
        sample=rand.sample(self.exp,n)
        fistS=[]
        actrew=[]
        nextS=[]
        for i,j,k,l,m in sample:
            #print("i\n",i,"j\n",j,"k\n",k,"l\n",l)
            ii=i.reshape(1,-1)
            mm=m.reshape(1,-1)
            #print("ii\n",ii,"ll\n",ll)
            fistS.append(ii)
            actrew.append((j,k,l))
            nextS.append(mm)

        return fistS,actrew,nextS
    
    def getSize(self):
        return len(self.exp)
