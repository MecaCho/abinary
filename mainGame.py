#-*-coding=UTF-8-*-
import pygame
import random
import time
import sys
import pygame, sys, random
from pygame.locals import *
from slideGame import slide_g
from matchGame import match_g
from morseGame import morseG
import Tkinter
from Tkinter import *

reload(sys)
sys.setdefaultencoding('utf-8')

# Create the constants (go ahead and experiment with different values)
TILESIZE = 100
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
FPS = 30
BLANK = None

#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)
BLUE =          (0,0,240)

SCREEN_SIZE = [WINDOWWIDTH,WINDOWHEIGHT]
WIDTH = 100
HEIGHT = 100
WAITING_TIME = 1000

BGCOLOR = BLUE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 28

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = 0
YMARGIN = 0


pygame.mixer.init()
bg_sound = pygame.mixer.Sound("plant.wav")
click_sound = pygame.mixer.Sound('click.wav')

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
pygame.init()
BASICFONT = pygame.font.Font('gkai00mp.ttf', BASICFONTSIZE)

FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption(u'伏羲')

DISPLAYSURF.fill(WHITE)
#pygame.draw.circle(screen,THECOLORS['blue'],[100,100],30,2)
background = pygame.Surface([600,500])
background.fill([0,0,255])
DISPLAYSURF.blit(background,(0,0))

def bgSoundPlay():
    pygame.mixer.init()
    bg_sound = pygame.mixer.Sound("plant.wav")
    bg_sound.play(loops=3)

def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

# Store the option buttons and their rectangles in OPTIONS.
exit1_SURF, exit1_RECT = makeText(u'退出', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 120)
help_SURF, help_RECT = makeText(u'帮助', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 120)
RESET_SURF, RESET_RECT = makeText(u'设置', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 90)
NEW_SURF, NEW_RECT = makeText(u'新游戏', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 60)
SOLVE_SURF, SOLVE_RECT = makeText(u'破解', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 30)
next_SURF, next_RECT = makeText(u'继续', TEXTCOLOR, TILECOLOR, 100, 0)
exit_SURF, exit_RECT = makeText(u'返回', TEXTCOLOR, TILECOLOR, 200, 0)

def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)

def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)


class background(pygame.sprite.Sprite):
    def __init__(self,filename,inittial_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect  = self.image.get_rect()
        self.rect.bottomright = inittial_position

tip_location = ([100,64],[210,64],[300,500],[410,500],[200,33],[310,33])
tip_Group = pygame.sprite.Group()
tip_Group.add(background('next.png',tip_location[4]))
tip_Group.add(background('reback.png',tip_location[5]))


DISPLAYSURF.blit(tip_Group.sprites()[0].image, tip_Group.sprites()[0].rect)
DISPLAYSURF.blit(tip_Group.sprites()[1].image, tip_Group.sprites()[1].rect)





def startFlash():
    start0 = pygame.image.load("start0.jpeg").convert_alpha()
    start1 = pygame.image.load("start1.jpg").convert_alpha()
    DISPLAYSURF.blit(start0, (0,0))
    pygame.display.flip()
    pygame.display.update()

def start0():
    start0 = pygame.image.load("start0.jpeg").convert_alpha()
    DISPLAYSURF.blit(start0, (0, 0))
    pygame.display.flip()
    pygame.display.update()
    start_board()

def show_help(filename='1.png',imagelocation=[100,100]):
    print 'True'
    imagep = pygame.image.load(filename)
    rect = imagep.get_rect()
    rect.bottomright = imagelocation
    screen.blit(imagep,rect)

def start_board():
    bg_location = ([150,34],[175,69],[150,105],[170,140],[WINDOWWIDTH,34],[WINDOWWIDTH,69],[WINDOWWIDTH,WINDOWHEIGHT])
    bg_Group = pygame.sprite.Group()
    bg_Group.add(background('help.png',bg_location[4]))
    bg_Group.add(background('know.png',bg_location[5]))
    bg_Group.add(background('exit.png',bg_location[6]))
    bg_Group.add(background('game1.png', bg_location[0]))
    bg_Group.add(background('game2.png', bg_location[1]))
    bg_Group.add(background('game3.png', bg_location[2]))
    bg_Group.add(background('game4.png', bg_location[3]))
    #bg_Group.add(background('next.png',bg_location[4]))
    #bg_Group.add(background('reback.png',bg_location[5]))

    for bg in bg_Group.sprites():
        DISPLAYSURF.blit(bg.image,bg.rect)
    pygame.display.flip()
    pygame.display.update()

def showHwnd():
    top = Tkinter.Tk()
    top.title('Python Title')
    top.geometry('400x300')
    top.resizable(width=True, height=True)

    aLabel = Tkinter.Label(top, text='This is a Label')
    aLabel.grid(column=0, row=0)

    action = Tkinter.Button(top, text='Click')
    action.grid(column=1, row=1)

    # Code to add widgets will go here...
    top.mainloop()

startFlash()
start_board()
rank = 2
#bgSoundPlay()
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==pygame.MOUSEBUTTONDOWN:
            print event.pos
            clickxy = event.pos
        elif event.type==pygame.MOUSEBUTTONUP:
            if clickxy[0]<100 and clickxy[1]<34 and clickxy[0]>0 and clickxy[1]>0:
                showHwnd()
            elif clickxy[0] < 100 and clickxy[1] < 68 and clickxy[0] > 0 and clickxy[1] > 34:
                bg_sound.stop()
                matchg = match_g()
                matchg.run()
                startFlash()
                start_board()
            elif clickxy[0] < 100 and clickxy[1] < 102 and clickxy[0] > 0 and clickxy[1] > 68:
                bg_sound.stop()
                slide = slide_g(BOARDHEIGHT=rank, BOARDWIDTH=rank)
                slide.main()
                startFlash()
                start_board()
            elif clickxy[0] < 100 and clickxy[1] < 136 and clickxy[0] > 0 and clickxy[1] > 102:
                bg_sound.stop()
                morse_g = morseG()
                morse_g.main()





