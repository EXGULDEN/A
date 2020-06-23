import numpy

class SumTree:

    def __init__(self,capacity):
        self.write=0
        self.capacity=capacity
        self.flag=True
        self.tree=numpy.zeros(2*capacity-1)
        self.data=numpy.zeros(capacity,dtype=object)

    def propagate(self,idx,change):
        parent=(idx-1)//2
        self.tree[parent]+=change
        if parent!=0:
            self.propagate(parent,change)

    def retrieve(self,idx,s): 
        left=2*idx+1
        right=left+1
        if left>=len(self.tree):
            return idx
        if s<=self.tree[left]:
            return self.retrieve(left,s)
        else:
            return self.retrieve(right,s)

    def total(self):
        return self.tree[0]

    def add(self,p,data):
        idx=self.write+self.capacity-1
        self.data[self.write]=data
        self.update(idx,p)
        self.write+=1
        if self.write>=self.capacity:
            self.flag=False
            self.write=0

    def update(self,idx,p):
        change=p-self.tree[idx]
        self.tree[idx]=p
        self.propagate(idx,change)

    def get(self,s):
        idx=self.retrieve(0,s)
        dataIdx=idx-self.capacity+1
        return idx,self.tree[idx],self.data[dataIdx]





















    
        
            
