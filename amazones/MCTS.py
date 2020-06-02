from Situation import Situation
import copy
from random import choice
import math


class MCTS(object):

    def __init__(self,flag):
        self.flag=flag
        self.C=math.sqrt(2)

    def Move(self,sit):
        sit.Show()
        if sit.Win():
            return
        for i in range(300):
            self.Choose(sit)
    def Choose(self,sit):
        if sit.Win():
            sit.UpNum(self.flag!=sit.flag)
            return 0-sit.flag
        child=sit.GetChild()
        if child:
            for c in child:
                if c.allnum==0:
                    ans=self.randWin(c)
                    sit.UpNum(self.flag==ans)
                    return ans
            nt=self.next(sit)
            ans=self.Choose(nt)
            sit.UpNum(self.flag==ans)
            return ans       
        else:
            self.CreatChild(sit)
            self.Choose(sit)

    def CreatChild(self,sit):
        if sit.flag==1:
            chess=sit.white
        elif sit.flag==-1:
            chess=sit.black
        
        for i in chess:
            ans=sit.Select(i.point.x,i.point.y)
            for j in ans:
                newsit=copy.deepcopy(sit)
                newsit.SetNum(0,0)
                newsit.Move(i.point.x,i.point.y,j.x,j.y)
                anss=newsit.Select(j.x,j.y)
                for k in anss:
                    newwsit=copy.deepcopy(newsit)
                    newwsit.Kill(k.x,k.y,anss)
                    sit.AddChild(newwsit)


    def randWin(self,situation):
        sit=copy.deepcopy(situation)
        win=sit.Win()
        while(win==False):
            chess=[]
            ans=[]
            if sit.flag==1:
                ans=sit.white
            elif sit.flag==-1:
                ans=sit.black
            for i in ans:
                if sit.Select(i.point.x,i.point.y):
                    chess.append(i)
            point=choice(chess)
            ans=sit.Select(point.point.x,point.point.y)
            move=choice(ans)
            sit.Move(point.point.x,point.point.y,move.x,move.y)
            ans=sit.Select(move.x,move.y)
            kill=choice(ans)
            sit.Kill(kill.x,kill.y,ans)
            win=sit.Win()
        situation.UpNum(self.flag!=sit.flag)
        return 0-sit.flag

    def next(self,sit):
        ans=0
        ma=0
        now=0
        if self.flag==sit.flag:
            for i in sit.child:
                if i.allnum==0:
                    now=0
                else:
                    now=i.winnum/i.allnum+self.C*math.sqrt(math.log(sit.allnum)/i.allnum)
                if now>ma:
                    ma=now
                    ans=i
        else:
            mi=1000
            for i in sit.child:
                if i.allnum==0:
                    now=1000
                else:
                    now=i.winnum/i.allnum+self.C*math.sqrt(math.log(sit.allnum)/i.allnum)
                if now<mi:
                    ma=now
                    ans=i
        return ans
    
    def nextt(self,sit):
        ch=sit.child
        ans=0
        if self.flag==1:
            mi=100000
            nowmi=0
            for i in ch:
                nowmi=0
                for j in i.black:
                    num=len(i.Select(j.point.x,j.point.y))
                    nowmi+=num
                if nowmi<mi:
                    mi=nowmi
                    ans=i
                    
            return ans
            
        if self.flag==-1:
            mi=100000
            nowmi=0
            for i in ch:
                nowmi=0
                for j in i.white:
                    num=len(i.Select(j.point.x,j.point.y))
                    nowmi+=num
                if nowmi<mi:
                    mi=nowmi
                    ans=i
            return ans
            


    def size(self,sit):
        i=1
        c=sit.child
        le=len(c)
        if c==0:
            return 1
        else:
            for j in c:
                i+=self.size(j)
            return i
            



    def Show(self,sit):
        i=0
        
        
        
        
        
