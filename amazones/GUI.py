import pygame
from pygame.locals import *
from Situation import Situation
from MCTS import MCTS
#from MCTSK import MCTSK
import math


WIDTH=50
N=10
stage=0
stage1=0
Sans=False
Nx=0
Ny=0
tree=0

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
    surf.blit(text_surface,(0,N*50+10))

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
situation=Situation(N)

#situation.SetChess(0,3)
#situation.SetChess(5,0)
#situation.SetChess(5,6)
#situation.Show()

while running:
    clock.tick(FPS)

    draw_background(screen,background,N)
    draw_Situation(screen,situation,N)
    draw_circle(screen,Sans,stage)
    if stage!=0 and situation.Win():
        print_winner(screen)
        stage=4

    
    if stage==1 and stage1==1 and situation.flag==tree.flag:
        tree.Move(situation)
        situation=tree.next(situation)
        tree.Move(situation)
    for event in pygame.event.get():
        if event.type == QUIT:
            running=False
        if event.type == KEYDOWN:
            if event.key==K_3:
                if stage==0:
                    N=3
                    situation=Situation(N)
                    screen = pygame.display.set_mode(((N+1)*50,(N+1)*50),0,32)
            if event.key==K_5:
                if stage==0:
                    N=5
                    situation=Situation(N)
                    screen = pygame.display.set_mode(((N+1)*50,(N+1)*50),0,32)
            if event.key==K_7:
                if stage==0:
                    N=7
                    situation=Situation(N)
                    screen = pygame.display.set_mode(((N+1)*50,(N+1)*50),0,32)
            if event.key==K_9:
                if stage==0:
                    N=9
                    situation=Situation(N)
                    screen = pygame.display.set_mode(((N+1)*50,(N+1)*50),0,32)
            if event.key==K_s and stage==0:
                stage=1
            if event.key==K_r:
                situation=Situation(N)
                stage=0
                stage1=0
                situation.SetChess(6,0)
                situation.SetChess(9,3)
                situation.SetChess(9,6)
                situation.SetChess(6,9)
            if event.key==K_z:
                if stage1!=1:
                    stage1=1
                    tree=MCTS(-1)
                    tree.Move(situation)
            if event.key==K_x:
                if stage1!=1:
                    stage1=1
                    tree=MCTS(1)
                    tree.Move(situation)
            if event.key==K_l:
                tree.Move(situation)
                si=tree.size(situation)
                print(si)
                if stage==1 and stage1==1 and situation.flag==tree.flag:
                    situation=tree.next(situation)
                tree.Move(situation)
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
