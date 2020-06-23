import pygame
from pygame.locals import *
from Situation import Situation
from MCTS import MCTS
from DeepQLearning import DeepQLearning
#from MCTSK import MCTSK
import math
import time


WIDTH=50
N=10
stage=0
stage1=0
Sans=False
Nx=0
Ny=0
tree=0
fistS=0
nextS=0
board=0
step=0
israndom=False
def draw_background(surf,background,N):
    surf.blit(background,(0,0))
    
    for i in range(0,N+1):
        pygame.draw.line(surf,(0,0,0),(10,i*WIDTH+10),(N*WIDTH+10,i*WIDTH+10))
    for i in range(0,N+1):
        pygame.draw.line(surf,(0,0,0),(i*WIDTH+10,10),(i*WIDTH+10,N*WIDTH+10))


def draw_Situation(surf,situation,N):
    for i in range(0,N):
        for j in range(0,N):
            if situation.board[i,j]==0:
                continue
            if situation.board[i,j]==1:
                surf.blit(white,(10+j*WIDTH,10+i*WIDTH))
            if situation.board[i,j]==-1:
                surf.blit(black,(10+j*WIDTH,10+i*WIDTH))
            if situation.board[i,j]==2:
                surf.blit(Xx,(10+j*WIDTH,10+i*WIDTH))

def draw_circle(surf,ans,f):
    if ans==False:
        return
    z=10+int(WIDTH/2)
    if f==2:
        for i in ans:
            pygame.draw.circle(surf,(0,0,255),(i.y*WIDTH+z,i.x*WIDTH+z),20,5)
    if f==3:
        for i in ans:
            pygame.draw.circle(surf,(255,0,0),(i.y*WIDTH+z,i.x*WIDTH+z),20,5)

def print_winner(surf):
    my_font = pygame.font.SysFont("arial", 26)
    
    if situation.flag==1:
        text_surface = my_font.render("winner is black!", True, (0,0,0))
    elif situation.flag==-1:
        text_surface = my_font.render("winner is white!", True, (0,0,0))
    time.sleep(1) 
    surf.blit(text_surface,(0,N*50+10))

def new_situation(N):
    situation=Situation(N)
    situation.SetChess(6,0)
    situation.SetChess(9,3)
    situation.SetChess(9,6)
    situation.SetChess(6,9)
    return situation

    

pygame.init()

screen = pygame.display.set_mode(((N+1)*50,(N+1)*50),0,32)

pygame.display.set_caption("Knight amazons!")
FPS=30
clock=pygame.time.Clock()

background=pygame.image.load("background.jpg")
black=pygame.image.load("b_knight.png").convert_alpha ()
white=pygame.image.load("w_knight.png").convert_alpha ()
Xx=pygame.image.load("Xx.png").convert_alpha ()
black=pygame.transform.scale(black, (50,50))
white=pygame.transform.scale(white, (50,50))
Xx=pygame.transform.scale(Xx, (50,50))
#w=pygame.transform.scale(white, (50,50))
running=True
situation=new_situation(N)
dqn=DeepQLearning()
x=0
y=0
xx=0
yy=0
xxx=0
yyy=0
while running:
    clock.tick(FPS)

    draw_background(screen,background,N)
    draw_Situation(screen,situation,N)
    draw_circle(screen,Sans,stage)
    if stage!=0 and situation.Win():
        print_winner(screen)
        stage=4
        if stage1==1:
            dqn.copy()
            dqn.saveModel('fistmodel.h5')
            situation=new_situation(N)
            stage=1


    #print("stage",stage,stage1)

    
    if stage1==1:
        print(stage)
        if stage==1:
            board=situation.GetBoard()
            numlist=situation.GetNum(-1)
            z,xx,yy,num=dqn.getNext(board,numlist,israndom)
            print("z",z)
            x,y=situation.GetXY(z)
            print(x,y,x+xx,y+yy,israndom)
            Sans=situation.Select(x,y)
            israndom=True
            if Sans:
                stage=2
                israndom=False
        if stage==2:
            t=False
            for i in Sans:
                if i.GetBool(x+xx,y+yy):
                    t=True
            if t:
                fistS=situation.board.copy()
                situation.Move(x,y,x+xx,y+yy)
                Sans=situation.Select(x+xx,y+yy)
                situation.SetBa(x+xx,y+yy)
                nextS=situation.board.copy()
                dqn.saveEXP(fistS,num,-1,0,nextS)
                xxx=x+xx
                yyy=y+yy
                stage=3
                israndom=False
            else:
                fistS=situation.board.copy()
                nextS=situation.board.copy()
                dqn.saveEXP(fistS,num,-100,1,nextS)
                stage=1
                israndom=True
        if stage==3:
            board=situation.GetBoard()
            numlist=situation.GetNum(1)
            z,xx,yy,num=dqn.getNext(board,numlist,israndom)
            fistS=situation.board.copy()
            print(xxx,yyy,x,y,x+xx,y+yy,israndom)
            if z>0:
                nextS=situation.board.copy()
                dqn.saveEXP(fistS,num,-100,1,nextS)
                israndom=True
            else:
                if situation.Kill(xx,yy,Sans):
                    situation.ResetBa()
                    nextS=situation.board.copy()
                    if situation.Win():
                        dqn.saveEXP(fistS,num,100*(0-situation.flag),1,nextS)
                    else:
                        dqn.saveEXP(fistS,num,-1,0,nextS)
                    dqn.learn()
                    stage=1
                    israndom=False
                else:
                    nextS=situation.board.copy()
                    dqn.saveEXP(fistS,num,-100,1,nextS)
                    israndom=True



                
    for event in pygame.event.get():
        if event.type == QUIT:
            running=False
        if event.type == KEYDOWN:
            if event.key==K_s and stage==0:
                stage=1
            if event.key==K_r:
                situation=new_situation(N)
                stage=1
            if event.key==K_l:
                print("dqn")
                stage1=1
                dqn.start()
                print(stage1)
            if event.key==K_k:
                print("dqn")
                stage1=1
                dqn.load('fistmodel.h5')
                print(stage1)
                
        if event.type == MOUSEBUTTONDOWN:
            y,x=pygame.mouse.get_pos()
            x=math.floor((x-10)/WIDTH)
            y=math.floor((y-10)/WIDTH)
            if stage==0:
                situation.SetChess(x,y)
            elif stage==1:
                Nx=x
                Ny=y
                Sans=situation.Select(x,y)
                if Sans:
                    stage=2
            elif stage==2:
                t=False
                for i in Sans:
                    if i.GetBool(x,y):
                        t=True
                if t:
                    situation.Move(Nx,Ny,x,y)
                    Sans=situation.Select(x,y)
                    stage=3
                else:
                    stage=1
            elif stage==3:
                if situation.Kill(x,y,Sans):
                    if stage1==1:
                        situation.ToNext()
                    if stage1==2:
                        situation=tree.next()
                    stage=1
                
                        
                

        

        pygame.display.update()




pygame.display.quit()
