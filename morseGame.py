#-*-coding=UTF-8-*-
import pygame
import random
import time
import sys
import string
import pygame, sys, random
import Tkinter
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
msg_font = pygame.font.Font('gkai00mp.ttf', 29)
output_font = pygame.font.Font('Arial.ttf', 19)

FPSCLOCK = pygame.time.Clock()



def makeText(text, color, bgcolor, top, left, font_=BASICFONT):
    # create the Surface and Rect objects for some text.
    textSurf = font_.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

input_SURF, input_RECT = makeText(u'输入:', TEXTCOLOR, TILECOLOR, 100, WINDOWHEIGHT - 400)
output_SURF, output_RECT = makeText(u'输出:', TEXTCOLOR, TILECOLOR, 100, WINDOWHEIGHT - 350)

translate_SURF, translate_RECT = makeText(u'翻译', TEXTCOLOR, TILECOLOR, 150, WINDOWHEIGHT - 200)
play_SURF, play_RECT = makeText(u'播放', TEXTCOLOR, TILECOLOR, 300, WINDOWHEIGHT - 200)
reset_SURF, reset_RECT = makeText(u'清空', TEXTCOLOR, TILECOLOR, 450, WINDOWHEIGHT - 200)

return_SURF, return_RECT = makeText(u'退出', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 140, WINDOWHEIGHT - 100)
help_SURF, help_RECT = makeText(u'帮助', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 140, WINDOWHEIGHT - 50)

class morseG(object):
    def __init__(self):
        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption(u'摩尔斯密码')

        self.DISPLAYSURF.fill(WHITE)
        # pygame.draw.circle(screen,THECOLORS['blue'],[100,100],30,2)
        self.background = pygame.Surface([800, 600])
        self.background.fill(BGCOLOR)
        self.DISPLAYSURF.blit(self.background, (0, 0))
        pygame.display.update()

    global input_SURF, input_RECT, output_SURF, output_RECT, translate_SURF, translate_RECT, play_SURF, play_RECT, pause_SURF, pause_RECT, reset_SURF, reset_RECT, exit1_SURF, exit1_RECT, help_SURF, help_RECT, return_SURF, return_RECT
    def bgSoundPlay(self):
        pygame.mixer.init()
        bg_sound = pygame.mixer.Sound("plant.wav")
        bg_sound.play(loops=3)

    def makeText(self,text, color, bgcolor, top, left,font_=BASICFONT):
        # create the Surface and Rect objects for some text.
        textSurf = font_.render(text, True, color, bgcolor)
        textRect = textSurf.get_rect()
        textRect.topleft = (top, left)
        return (textSurf, textRect)

    def showHwnd(self):
        top = Tkinter.Tk()
        top.title(u'知识卡片3')
        top.geometry('500x450')
        top.resizable(width=True, height=True)

        imgFile= './h2.gif'
        img = Tkinter.PhotoImage(file=imgFile)
        label1=Tkinter.Label(top,image=img)
        label1.grid(column=0, row=0)
        top.mainloop()


    def drawboard(self,msg = 'help cards',input_='',output_= ''):
        global input_SURF, input_RECT, output_SURF, output_RECT, translate_SURF, translate_RECT, play_SURF, play_RECT, pause_SURF, pause_RECT, reset_SURF, reset_RECT, exit1_SURF, exit1_RECT, help_SURF, help_RECT, return_SURF, return_RECT
        if msg:
            message_SURF,message_RECT = self.makeText(msg,MESSAGECOLOR, BGCOLOR, 5, 5,font_=msg_font)
            self.DISPLAYSURF.blit(message_SURF,message_RECT)
        if input_:
            input_SURF,input_RECT = self.makeText(input_,MESSAGECOLOR, BGCOLOR, 200, WINDOWHEIGHT - 390,font_=msg_font)
            self.DISPLAYSURF.blit(input_SURF,input_RECT)
        if output_:
            output_SURF,output_RECT = self.makeText(output_,MESSAGECOLOR, BGCOLOR, 200, WINDOWHEIGHT - 334,font_=output_font)
            self.DISPLAYSURF.blit(output_SURF,output_RECT)

        self.DISPLAYSURF.blit(translate_SURF, translate_RECT)
        self.DISPLAYSURF.blit(play_SURF, play_RECT)
        self.DISPLAYSURF.blit(reset_SURF, reset_RECT)

        self.DISPLAYSURF.blit(input_SURF, input_RECT)
        self.DISPLAYSURF.blit(output_SURF, output_RECT)

        self.DISPLAYSURF.blit(return_SURF, return_RECT)
        self.DISPLAYSURF.blit(help_SURF, help_RECT)
        pygame.display.update()

    def getLeftTopOfTile(self,tileX, tileY):
        left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
        top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
        return (left, top)

    def drawTile(self,tilex, tiley, number, adjx=0, adjy=0):
        # draw a tile at board coordinates tilex and tiley, optionally a few
        # pixels over (determined by adjx and adjy)
        left, top = self.getLeftTopOfTile(tilex, tiley)
        pygame.draw.rect(self.DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
        textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
        textRect = textSurf.get_rect()
        textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
        self.DISPLAYSURF.blit(textSurf, textRect)

    def translateChars(self,inputChar = ''):
        codeDic = [".-", "-...", "-.-.", "-..", ".", "..-.",
           "--.", "....", "..", ".---", "-.-", ".-..", "--", "-.",
           "---", ".--.", "--.-", ".-.", "...", "-", "..-", "...-",
           ".--", "-..-", "-.--", "--.."]
        outputChar = ''
        for ch in inputChar:
            ch = string.upper(ch)
            outputChar += codeDic[ord(ch)-ord('A')]
            outputChar += '/'
        return outputChar

    def searchMs(self,ch=''):
        codeDic = [".-", "-...", "-.-.", "-..", ".", "..-.",
           "--.", "....", "..", ".---", "-.-", ".-..", "--", "-.",
           "---", ".--.", "--.-", ".-.", "...", "-", "..-", "...-",
           ".--", "-..-", "-.--", "--.."]
        for i in xrange(26):
            if ch == codeDic[i]:
                return chr(i+65)
        return 0

    def translateMorse(self,inputMorse = ''):
        outputChar = ''
        tmp = ''
        letters = ''
        if inputMorse.find('/') != -1:
            inputMorse = inputMorse.split('/')
        elif inputMorse.find(' ') != -1:
            inputMorse = inputMorse.split(' ')
        print inputMorse
        if type(inputMorse) == list:
            for ch in inputMorse:
                tmp = ch
                print tmp
                tmp = tmp.strip('/ ')
                print tmp
                le = self.searchMs(tmp)
                print 'letter : ',le
                if le:
                    letters += self.searchMs(tmp)
                else:
                    return u'输入有误'
                tmp = ''
            outputChar += letters
        else:
            outputChar = self.searchMs(inputMorse)
        return outputChar

    def morseplay(self,str_input=''):
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

    def main(self):
        global input_txt,output_txt
        input_txt = ''
        output_txt = ''
        running  = True
        while running:
            msg_text = u'输入数字、字母、标点符号、或摩尔斯密码符号‘-’、‘.’'
            self.drawboard(msg=msg_text, input_=input_txt, output_=output_txt)
            running = self.handleEvents()
        return

    def handleEvents(self):
        global input_txt, output_txt
        flag = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.clicked = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if translate_RECT.collidepoint(self.clicked):
                    if not output_txt:
                        output_txt = self.translateChars(input_txt)
                    elif not input_txt:
                        input_txt = self.translateMorse(output_txt)
                        # self.morseplay(output_txt)
                elif play_RECT.collidepoint(self.clicked):
                    output_txt = self.translateChars(input_txt)
                    self.morseplay(output_txt)
                elif reset_RECT.collidepoint(self.clicked):
                    # self.morseplay(output_txt)
                    flag = 1
                    output_txt = ' ' * 100
                    input_txt = ' ' * 100
                elif return_RECT.collidepoint(self.clicked):
                    # print output_txt
                    return False
                elif help_RECT.collidepoint(self.clicked):
                    # print output_txt
                    self.showHwnd()
            elif event.type == KEYUP:
                if flag:
                    input_txt = ''
                    flag = 0
                    output_txt = ''
                if event.key in (
                K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m, K_n, K_o, K_p, K_q, K_r,
                K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z):
                    key_value = chr(event.key)
                    print event.key, key_value
                    input_txt = str(input_txt) + str(key_value)
                    print input_txt
                elif event.key in (K_MINUS, K_PERIOD, K_SPACE, K_SLASH):
                    key_value = chr(event.key)
                    print event.key, key_value
                    output_txt = str(output_txt) + str(key_value)
                    print output_txt
                    print event.key
                else:
                    print event.key
        return True


if __name__ == '__main__':
    morse_g = morseG()
    morse_g.main()
