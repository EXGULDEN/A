from Point import Point
class Chess(object):
    
    def __init__(self,x,y,colour):
        self.point=Point(x,y)
        self.colour=colour
        
    def GetMove(self):
        ans=[]
        anss=[]
        for i in range(1,10):
            anss.append(Point(self.point.x,self.point.y+i))
        ans.append(anss)
        anss1=[]
        for i in range(1,10):
            anss1.append(Point(self.point.x+i,self.point.y+i))
        ans.append(anss1)
        anss2=[]
        for i in range(1,10):
            anss2.append(Point(self.point.x+i,self.point.y))
        ans.append(anss2)
        anss3=[]
        for i in range(1,10):
            anss3.append(Point(self.point.x+i,self.point.y-i))
        ans.append(anss3)
        anss4=[]
        for i in range(1,10):
            anss4.append(Point(self.point.x,self.point.y-i))
        ans.append(anss4)
        anss5=[]
        for i in range(1,10):
            anss5.append(Point(self.point.x-i,self.point.y-i))
        ans.append(anss5)
        anss6=[]
        for i in range(1,10):
            anss6.append(Point(self.point.x-i,self.point.y))
        ans.append(anss6)
        anss7=[]
        for i in range(1,10):
            anss7.append(Point(self.point.x-i,self.point.y+i))
        ans.append(anss7)
        return ans

    def GetBool(self,x,y):
        return self.point.GetBool(x,y)

    def Change(self,x,y):
        self.point.Change(x,y)
        
    def Show(self):
        print(self.point.x,self.point.y)
