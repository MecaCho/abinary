#-*-coding=UTF-8-*-
import pygame
import random
import time
import sys
import pygame, sys, random
from pygame.locals import *
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
BASICFONTSIZE = 39

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = 0
YMARGIN = 0


pygame.mixer.init()
da_sound = pygame.mixer.Sound("da.wav")
di_sound = pygame.mixer.Sound("di.wav")
click_sound = pygame.mixer.Sound('click.wav')


UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
pygame.init()
BASICFONT = pygame.font.Font('gkai00mp.ttf', BASICFONTSIZE)
msg_font = pygame.font.Font('gkai00mp.ttf', 28)

FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption(u'伏羲')

DISPLAYSURF.fill(WHITE)
#pygame.draw.circle(screen,THECOLORS['blue'],[100,100],30,2)
background = pygame.Surface([800,600])
background.fill([0,0,255])
DISPLAYSURF.blit(background,(0,0))
pygame.display.update()

def bgSoundPlay():
    pygame.mixer.init()
    bg_sound = pygame.mixer.Sound("plant.wav")
    bg_sound.play(loops=3)

def makeText(text, color, bgcolor, top, left,font_=BASICFONT):
    # create the Surface and Rect objects for some text.
    textSurf = font_.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

exit1_SURF, exit1_RECT = makeText(u'退出', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 120)
help_SURF, help_RECT = makeText(u'帮助', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 120)

translate_SURF, translate_RECT = makeText(u'翻译', TEXTCOLOR, TILECOLOR, 200, WINDOWHEIGHT - 200)
play_SURF, play_RECT = makeText(u'播放', TEXTCOLOR, TILECOLOR, 400, WINDOWHEIGHT - 200)
pause_SURF, pause_RECT = makeText(u'暂停', TEXTCOLOR, TILECOLOR, 600, WINDOWHEIGHT - 200)

def drawboard(msg = 'help cards',input_='',output_= ''):
    global translate_SURF, translate_RECT
    if msg:
        message_SURF,message_RECT = makeText(msg,MESSAGECOLOR, BGCOLOR, 5, 5,font_=msg_font)
        DISPLAYSURF.blit(message_SURF,message_RECT)
    if input_:
        input_SURF,input_RECT = makeText(input_,MESSAGECOLOR, BGCOLOR, 90, 90,font_=msg_font)
        DISPLAYSURF.blit(message_SURF,message_RECT)
    exit1_SURF, exit1_RECT = makeText(u'退出', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 120)
    help_SURF, help_RECT = makeText(u'帮助', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 120)

    translate_SURF, translate_RECT = makeText(u'翻译', TEXTCOLOR, TILECOLOR, 200, WINDOWHEIGHT - 200)
    play_SURF, play_RECT = makeText(u'播放', TEXTCOLOR, TILECOLOR, 400, WINDOWHEIGHT - 200)
    pause_SURF, pause_RECT = makeText(u'暂停', TEXTCOLOR, TILECOLOR, 600, WINDOWHEIGHT - 200)

    input_SURF, input_RECT = makeText(u'输入:'+input_, TEXTCOLOR, TILECOLOR, 100, WINDOWHEIGHT - 400)
    output_SURF, output_RECT = makeText(u'输出:'+output_, TEXTCOLOR, TILECOLOR, 100, WINDOWHEIGHT - 350)

    DISPLAYSURF.blit(translate_SURF, translate_RECT)
    DISPLAYSURF.blit(play_SURF, play_RECT)
    DISPLAYSURF.blit(pause_SURF, pause_RECT)
    DISPLAYSURF.blit(input_SURF, input_RECT)
    DISPLAYSURF.blit(output_SURF, output_RECT)
    pygame.display.update()

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

def morseplay(str_input=''):
    for str in str_input:
        if str == '.':
            di_sound.play()
            print 'di'
            time.sleep(0.3)
        elif str == '-':
            da_sound.play()
            time.sleep(0.3)
            print 'da'
        elif str == '/':
            time.sleep(0.6)
        else:
            time.sleep(0.3)
            print 'sleep'

running  = True
input_txt = ''
output_txt = ''
while running:
    key_value = ''
    msg_text=u'输入数字、字母、标点符号、或摩尔斯密码符号‘-’、‘.’'
    drawboard(msg=msg_text,input_=input_txt,output_=output_txt)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if translate_RECT.collidepoint(event.pos):
                output_txt = 'output'
            di_sound.play(loops=1)
            time.sleep(0.5)
            da_sound.play(loops=1)
            time.sleep(1)
            morseplay('-.-/.-.')
            print clicked
            print output_txt
        elif event.type == KEYUP:
            # check if the user pressed a key to slide a tile
            if event.key in ( K_a,K_b,K_c,K_d,K_e,K_f,K_g,K_h,K_i,K_j,K_k,K_l,K_m,K_n,K_o,K_p,K_q,K_r,K_s,K_t,K_u,K_v,K_w,K_x,K_y,K_z):
                key_value = chr(event.key)
                print event.key,key_value
                input_txt = str(input_txt)+str(key_value)
                print input_txt



