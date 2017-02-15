#-*-coding=UTF-8-*-
import pygame
from sys import exit
from pygame.locals import *
pygame.init()
backgroundImage_start = 'the_background.gif'
backgroundImage_FuHsi = ''
backgroundImage_1 = 'background_1.png'
backgroundImage_2 = ''
backgroundImage_3 = ''

screenSize=(640,480)
########################(分辨率，标志位，色深)FULLSCREEN创建一个全屏窗口
####DOUBLEBUF 	创建一个“双缓冲”窗口，建议在HWSURFACE或者OPENGL时使用
#HWSURFACE 	创建一个硬件加速的窗口，必须和FULLSCREEN同时使用
#OPENGL 	创建一个OPENGL渲染的窗口
#RESIZABLE 	创建一个可以改变大小的窗口
#NOFRAME 	创建一个没有边框的窗口
screen = pygame.display.set_mode(screenSize,0,32)
pygame.display.set_caption("FuHsi")
background_start = pygame.image.load(backgroundImage_start)
background_1 = pygame.image.load(backgroundImage_1)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.blit(background_start,(0,0))
    pygame.display.update()
    if event.type == pygame.MOUSEBUTTONDOWN:
        print event.pos
        xy = event.pos
    elif event.type == pygame.MOUSEBUTTONUP:
        screen.blit(background_1,xy)
        pygame.display.update()
    '''elif event.type == pygame.MOUSEBUTTONDOWN:
        print event.pos
        self.clicked = event.pos
        # store position
    elif event.type == pygame.MOUSEBUTTONUP:'''




