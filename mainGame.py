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
GREEN =         (  0, 255,   0)
darkGreen =     (0,100,0)
BLUE =          (0,0,240)

SCREEN_SIZE = [WINDOWWIDTH,WINDOWHEIGHT]
WIDTH = 100
HEIGHT = 100
WAITING_TIME = 1000

BGCOLOR = BLUE
TILECOLOR = darkGreen
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 28
titleFontSize = 43

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
titleFONT = pygame.font.Font('gkai00mp.ttf', titleFontSize)

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
    textSurf = titleFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

# Store the option buttons and their rectangles in OPTIONS.
game1_SURF, game1_RECT = makeText(u'伏羲的启示', TEXTCOLOR, TILECOLOR, WINDOWWIDTH*0.1, 20)
game2_SURF, game2_RECT = makeText(u'神奇的八卦', TEXTCOLOR, TILECOLOR, WINDOWWIDTH*0.1, 80)
game3_SURF, game3_RECT = makeText(u'8421', TEXTCOLOR, TILECOLOR, WINDOWWIDTH*0.1, 140)
game4_SURF, game4_RECT = makeText(u'摩尔斯密码', TEXTCOLOR, TILECOLOR, WINDOWWIDTH*0.1, 200)
exit1_SURF, exit1_RECT = makeText(u'退出', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 140, WINDOWHEIGHT - 120)
help_SURF, help_RECT = makeText(u'帮助', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 140, WINDOWHEIGHT - 120)
RESET_SURF, RESET_RECT = makeText(u'设置', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 140, WINDOWHEIGHT - 90)
NEW_SURF, NEW_RECT = makeText(u'新游戏', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 140, WINDOWHEIGHT - 60)
SOLVE_SURF, SOLVE_RECT = makeText(u'破解', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 140, WINDOWHEIGHT - 30)
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
    DISPLAYSURF.blit(imagep,rect)

def start_board():
    DISPLAYSURF.blit(game1_SURF, game1_RECT)
    DISPLAYSURF.blit(game2_SURF, game2_RECT)
    DISPLAYSURF.blit(game3_SURF, game3_RECT)
    DISPLAYSURF.blit(game4_SURF, game4_RECT)
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
            if game1_RECT.collidepoint(event.pos):
                showHwnd()
            elif game2_RECT.collidepoint(event.pos):
                bg_sound.stop()
                matchg = match_g()
                matchg.run()
                startFlash()
                start_board()
            elif game3_RECT.collidepoint(event.pos):
                bg_sound.stop()
                slide = slide_g(BOARDHEIGHT=rank, BOARDWIDTH=rank)
                slide.main()
                startFlash()
                start_board()
            elif game4_RECT.collidepoint(event.pos):
                bg_sound.stop()
                morse_g = morseG()
                morse_g.main()





