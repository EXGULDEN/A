import multiprocessing as mp
import threading as th
from queue import Queue

from Situation import Situation
from DeepQLearning import DeepQLearning
import math
import time



N=10
stage=1
stage1=1
Sans=False
Nx=0
Ny=0
tree=0
fistS=0
nextS=0
board=0
step=0
israndom=False


def print_winner():

    
    if situation.flag==1:
        print("winner is black!")
    elif situation.flag==-1:
        print("winner is white!")

def new_situation(N):
    situation=Situation(N)
    situation.SetChess(6,0)
    situation.SetChess(9,3)
    situation.SetChess(9,6)
    situation.SetChess(6,9)
    return situation
    




situation=new_situation(N)
dqn=DeepQLearning()
dqn.start()




def Workers(exp,nn,l):
    running=True
    dqn=DeepQLearning(0)
    x=0
    y=0
    xx=0
    yy=0
    xxx=0
    yyy=0
    step=0
    stage=1
    stage1=1
    situation=new_situation(N)

    while running:


        if step==1100000:
            running=False

        if step%200==0:
            l.acquire()
            dqn.copym(nn.get())
            l.release()

    
        if stage!=0 and situation.Win():
            print_winner()
            stage=4
            if stage1==1:
                situation=new_situation(N)
                stage=1
    
        if stage1==1:
            if stage==1:
                board=situation.GetBoard()
                numlist=situation.GetNum(-1)
                num,x,y,xx,yy=dqn.getNext(board,numlist,israndom)

                Sans=situation.Select(x,y)
                israndom=True
                if Sans:
                    stage=2
                    israndom=False
            if stage==2:
                t=False
                for i in Sans:
                    if i.GetBool(xx,yy):
                        t=True
                if t:
                    fistS=situation.board.copy()
                    situation.Move(x,y,xx,yy)
                    Sans=situation.Select(xx,yy)
                    situation.SetBa(xx,yy)
                    nextS=situation.board.copy()
                    l.acquire() 
                    exp.put(fistS)
                    exp.put(num)
                    exp.put(-1)
                    exp.put(0)
                    exp.put(nextS)
                    l.release()
                    xxx=xx
                    yyy=yy
                    stage=3
                    israndom=False
                else:
                    fistS=situation.board.copy()
                    nextS=situation.board.copy()
                    l.acquire()
                    exp.put(fistS)
                    exp.put(num)
                    exp.put(-100)
                    exp.put(1)
                    exp.put(nextS)
                    l.release()
                    stage=1
                    israndom=True
            if stage==3:
                board=situation.GetBoard()
                numlist=situation.GetNum(1)
                num,xx,yy,xx_,yy_=dqn.getNext(board,numlist,israndom)
                fistS=situation.board.copy()
                if xx!=xx_ or yy!=yy_:
                    nextS=situation.board.copy()
                    l.acquire()
                    exp.put(fistS)
                    exp.put(num)
                    exp.put(-100)
                    exp.put(1)
                    exp.put(nextS)
                    l.release()
                    israndom=True
                else:
                    if situation.Kill(xx,yy,Sans):
                        situation.ResetBa()
                        nextS=situation.board.copy()
                        if situation.Win():
                            r=situation.getReword()
                            l.acquire()
                            exp.put(fistS)
                            exp.put(num)
                            exp.put(100*(0-situation.flag)+r)
                            exp.put(1)
                            exp.put(nextS)
                            l.release()
                        else:
                            r=situation.getReword()
                            l.acquire()
                            exp.put(fistS)
                            exp.put(num)
                            exp.put(r)
                            exp.put(0)
                            exp.put(nextS)
                            l.release()
                        stage=1
                        israndom=False
                    else:
                        nextS=situation.board.copy()
                        r=situation.getReword()
                        l.acquire()
                        exp.put(fistS)
                        exp.put(num)
                        exp.put(-100)
                        exp.put(1)
                        exp.put(nextS)
                        l.release()
                        israndom=True
                step+=1


def Tree(exp):
    global dqn
    global run
    while run:
        print(exp.empty())
        if exp.empty()==False:
            fists=exp.get()
            num=exp.get()
            r=exp.get()
            fn=exp.get()
            nexts=exp.get()
            dqn.saveEXP(fists,num,r,fn,nexts)
            print("aaa",dqn.exp.tree.write)


def Learner(nn):
    global dqn
    step=0
    run=True
    print("in")
    for i in range(8):
        nn.put(dqn.getmWeight())
    while run:
        if dqn.exp.tree.flag==False:
            run=False
        #print(dqn.exp.tree.write)
    run=True
    while run:
        if step==1000000:
            run=False
        if step%200==0:
            for i in range(4):
                nn.put(dqn.getmWeight())
        dqn.learn()
        step+=1

                
                        
                
if __name__=='__main__':

    l=mp.Lock()
    run=True
    dqn=DeepQLearning()
    dqn.start()
    exp=mp.Queue()
    nn=mp.Queue()
    learn=th.Thread(target=Learner,args=(nn,))
    tree=th.Thread(target=Tree,args=(exp,))
    worker1=mp.Process(target=Workers,args=(exp,nn,l,))
    worker2=mp.Process(target=Workers,args=(exp,nn,l,))
    worker3=mp.Process(target=Workers,args=(exp,nn,l,))
    worker4=mp.Process(target=Workers,args=(exp,nn,l,))
    
    learn.start()
    tree.start()
    worker1.start()
    worker2.start()
    worker3.start()
    worker4.start()
    learn.join()
    tree.join()
    worker1.join()
    worker2.join()
    worker3.join()
    worker4.join()
    dqn.saveModel("pmodle")
    


