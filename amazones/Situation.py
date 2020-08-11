from Chess import Chess
from numpy import *

class Situation(object):
    
    def __init__(self,n=5):
        self.n=n
        self.board=zeros([self.n,self.n],int)
        self.white=[]
        self.black=[]
        self.flag=1
        self.child=[]
        self.winnum=0
        self.allnum=0
        
    def SetChess(self,x,y):
        if self.NotInBoard(x,y,self.n):
            return False
        if self.board[x,y]!=0:
            return False
        if x==y and x==int((self.n-1)/2):
            return False
        white=Chess(x,y,1)
        self.white.append(white)
        self.board[x,y]=1
        xx=self.n-1-x
        yy=self.n-1-y
        black=Chess(xx,yy,-1)
        self.black.append(black)
        self.board[xx,yy]=-1

    def Select(self,x,y):
        if self.NotInBoard(x,y,self.n):
            return False
        if self.board[x,y]!=self.flag:
            return False
        ans=[]
        anss=[]
        if self.board[x,y]==1:
            for i in self.white:
                if i.GetBool(x,y):
                    anss=i.GetMove()
        if self.board[x,y]==-1:
            for i in self.black:
                if i.GetBool(x,y):
                    anss=i.GetMove()
        for j in anss:
            for i in j:
                if i.InBoard(self.n)==False:
                    break
                if self.board[i.x,i.y]!=0:
                    break
                if self.board[i.x,i.y]==0:
                    ans.append(i)
        return ans

    def Kill(self,x,y,l):
        for i in l:
            if i.GetBool(x,y):
                self.board[x,y]=2
                self.flag=0-self.flag
                return True
        return False

    def Move(self,x,y,xx,yy):
        self.board[xx,yy]=self.board[x,y]
        if self.board[x,y]==1:
            for i in self.white:
                if i.GetBool(x,y):
                    i.Change(xx,yy)
                    self.board[x,y]=0
                    return True
        if self.board[x,y]==-1:
            for i in self.black:
                if i.GetBool(x,y):
                    i.Change(xx,yy)
                    self.board[x,y]=0
                    return True
        return False

    def Win(self):
        if self.flag==1:
            for i in self.white:
                if self.Select(i.point.x,i.point.y):
                    return False
        if self.flag==-1:
            for i in self.black:
                if self.Select(i.point.x,i.point.y):
                    return False
        return True

    def NotInBoard(self,x,y,n):
        if x<0 or x>=n or y<0 or y >=n:
            return True
        else:
            return False

    def GetStr(self):
        return self.board.tostring()

    def GetXY(self,z):
        if z<0:
            return -20,-20
        if self.flag==1:
            return self.white[z].point.x,self.white[z].point.y
        elif self.flag==-1:
            return self.black[z].point.x,self.black[z].point.y

    def GetBoard(self):
        if self.flag==1:
            b=self.board
            return b.reshape(1,-1)
        else:
            a=where(self.board!=4,0,4)
            b=where(self.board!=2,0,2)
            c=self.board*-1+b*2+a*2
            return c.reshape(1,-1)
        

    def AddChild(self,sit):
        self.child.append(sit)

    def GetChild(self):
        return self.child

    def SetNum(self,x,y):
        self.child=[]
        self.winnum=0
        self.allnum=0

    def UpNum(self,flag):
        self.allnum+=1
        if flag:
            self.winnum+=1

    def ToNext(self):
        if self.child: 
            string=self.GetStr()
            for i in self.child:
                if string==i.GetStr():
                    self.child=i.child

    def GetNum(self,flag,sflag=0):
        ans=[]
        if sflag==0:
            sflag=self.flag
        if flag<0:
            if sflag==1:
                chess=self.white
            elif sflag==-1:
                chess=self.black
            for i in range(4):
                nu=chess[i].GetMove()
                for j in nu:
                    f=True
                    for k in j:
                        if f:
                            if k.InBoard(self.n)==False:
                                f=False
                                continue
                            if self.board[k.x,k.y]!=0:
                                f=False
                                continue
                            if self.board[k.x,k.y]==0:
                                ans.append([chess[i].point.x,chess[i].point.y,k.x,k.y])
        else:
            for i in range(10):
                for j in range(10):
                    if self.board[i][j]==4:
                        ans.append([i,j,i,j])
        return ans

    def SetBa(self,x,y):
        Ba=self.Select(x,y)
        for i in Ba:
            self.board[i.x,i.y]=4
            
    def ResetBa(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j]==4:
                    self.board[i][j]=0

    def getReword(self):
        wr=len(self.GetNum(-1,1))
        br=len(self.GetNum(-1,-1))
        ans=0
        if self.flag==1:
            ans=(wr-br)*10
        if self.flag==-1:
            ans=(br-wr)*10
        return ans
                    
            
            
        
    def Show(self):
        #for i in self.child:
         #   print(i.board)
        print(self.board)
