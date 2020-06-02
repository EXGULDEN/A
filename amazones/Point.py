
class Point(object):
    
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def InBoard(self,n):
        if self.x>=0 and self.x<=n-1 and self.y>=0 and self.y <=n-1:
            return True
        else:
            return False

    def GetBool(self,x,y):
        if self.x==x and self.y==y:
            return True
        else:
            return False

    def Change(self,x,y):
        self.x=x
        self.y=y
        
    def Show(self):
        print(self.x,self.y)
