#-*-coding=UTF-8-*-
import pygame
import random
import time
import sys
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
WAITING_TIME = 200

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
pygame.display.set_caption(u'神奇的八卦')

DISPLAYSURF.fill(BRIGHTBLUE)
#pygame.draw.circle(screen,THECOLORS['blue'],[100,100],30,2)
#background = pygame.Surface([WINDOWWIDTH,WINDOWHEIGHT])
#background.fill([0,0,255])
#DISPLAYSURF.blit(background,(0,0))

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
help_SURF, help_RECT = makeText(u'帮助', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 90)
NEW_SURF, NEW_RECT = makeText(u'新游戏', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 60)
SOLVE_SURF, SOLVE_RECT = makeText(u'破解', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 30)
next_SURF, next_RECT = makeText(u'继续', TEXTCOLOR, TILECOLOR, 100, 100)
exit_SURF, exit_RECT = makeText(u'返回', TEXTCOLOR, TILECOLOR, 200, 100)

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

'''tip_location = ([100,64],[210,64])
tip_Group = pygame.sprite.Group()
tip_Group.add(background('next.png',tip_location[0]))
tip_Group.add(background('reback.png',tip_location[1]))


DISPLAYSURF.blit(tip_Group.sprites()[0].image, tip_Group.sprites()[0].rect)
DISPLAYSURF.blit(tip_Group.sprites()[1].image, tip_Group.sprites()[1].rect)'''


class Card(pygame.sprite.Sprite):
    "It's the card to see matching game. Has 2 sides, check em"
    def __init__(self, xy, card_pic, value):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(card_pic)
        self.rect = self.image.get_rect()
        self.value = value
        self.rect.left, self.rect.top = xy
        self.rect.width, self.rect.height = WIDTH, HEIGHT
        self.is_displayed = False


class match_g(object):
    def __init__(self):
        global rightCards
        rightCards = []
        self.clock = pygame.time.Clock()
        self.winning_font = BASICFONT
        pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP])
        self.corresponding_position_list = []
        self.drawBackground()
        self.sprites = pygame.sprite.RenderUpdates()

        self.value_list = []
        for i in range(0, 16, 1):
            self.value_list.append(i)
        random.shuffle(self.value_list)
        print self.value_list
        ctr = -1

        self.card_list = []
        for pos in range(0, 16, 1):
            val = (self.value_list[pos]) + 1
            self.card_list.append(Card(self.corresponding_position_list[pos], "%s.gif" % val, val))
        for card in self.card_list:
            self.sprites.add(card)
        self.sprites = pygame.sprite.RenderUpdates()

    def drawtips(self,message, drawp='',durTime=0):
        global dur_time
        dur_time = durTime
        #print dur_time
        dur_time = str(int(round(durTime/3600,0)))+':'+str(int(round(durTime/60,0)))+':'+str(int(round(durTime%60,0)))
        #print dur_time
        time_SURF, time_RECT = makeText(u'用时：' + dur_time, TEXTCOLOR, TILECOLOR, 0, 70)
        if message:
            textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
            self.mbackground.blit(textSurf, textRect)
        if drawp:
            self.mbackground.blit(next_SURF, next_RECT)
            self.mbackground.blit(exit_SURF, exit_RECT)
        self.mbackground.blit(time_SURF, time_RECT)
        DISPLAYSURF.blit(self.mbackground, (0, 0))
        pygame.display.flip()

    def showHwnd(self):
        hwnd = Tkinter.Tk()
        hwnd.mainloop()

    def drawCard(self, position):
        self.sprites.add(self.card_list[position])
        self.sprites.draw(self.mbackground)
        DISPLAYSURF.blit(self.mbackground, (0, 0))
        pygame.display.flip()

    def drawCards(self):
        self.sprites.draw(self.mbackground)
        DISPLAYSURF.blit(self.mbackground, (0, 0))
        pygame.display.flip()

    def drawBackground(self):
        global rightCards
        self.mbackground = pygame.Surface(SCREEN_SIZE)
        self.mbackground.fill(BLUE)
        self.bagua_image = pygame.image.load('bagua.png')
        #self.mbackground.blit(self.bagua_image, (0, 0))
        self.blank_card = pygame.Surface((WIDTH, HEIGHT))
        self.blank_card.fill(GREEN)
        for x in range(200, 600, WIDTH + 1):
            for y in range(100, 500, HEIGHT + 1):
                self.corresponding_position_list.append((x, y))
                cardSq = (x-200)/WIDTH*4+(y-100)/HEIGHT
                self.mbackground.blit(self.blank_card, (x, y))

        self.mbackground.blit(help_SURF, help_RECT)
        self.mbackground.blit(NEW_SURF, NEW_RECT)
        self.mbackground.blit(SOLVE_SURF, SOLVE_RECT)
        DISPLAYSURF.blit(self.mbackground, (0, 0))
        pygame.display.flip()

    def run(self):
        global msg,opened_cards,rightCards
        msg = u'点击两个方块，若找到两个匹配的则翻开，直到翻开全部方块'  # contains the message to show in the upper left corner.
        drawp = ''
        running = True
        # game will only change if event happens
        self.clicked = (-1, -1)
        opened_cards = []
        rightCards = []
        # bgSoundPlay()
        self.drawtips(msg, drawp)
        now = time.time()
        while running:
            timeDur = round(time.time()-now,0)
            self.drawtips(msg, drawp,durTime=timeDur)
            running = self.handleEvents()
        return

    def searchCard(self,eventPos):
        eventpos = eventPos
        self.clicked = eventPos
        which_card = 0
        for x in range(200, 600, WIDTH + 1):
            for y in range(100, 500, HEIGHT + 1):
                if eventPos[0]<x+WIDTH and eventPos[0]>x and eventPos[1]<y+HEIGHT and eventPos[1]>y:
                    return (x-200)/WIDTH*4 + (y-100)/HEIGHT
        return -1

    def handleEvents(self):
        global msg,opened_cards,rightCards,dur_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play(loops=1)
                #print event.pos
                self.clicked = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if help_RECT.collidepoint(event.pos):
                    msg='help info'
                    self.showHwnd()
                elif SOLVE_RECT.collidepoint(event.pos):
                    msg = 'solve info'
                elif NEW_RECT.collidepoint(event.pos):
                    return
                elif self.searchCard(eventPos=event.pos) != -1:
                    #print self.searchCard(eventPos=event.pos)
                    which_card=self.searchCard(eventPos=event.pos)
                    if not self.card_list[which_card] in self.sprites:
                        opened_cards.append(self.card_list[which_card])
                        #self.sprites.remove(opened_cards)
                        self.drawCard(which_card)
                        if len(opened_cards) == 2:
                            if opened_cards[0].value % 8 == opened_cards[1].value % 8:
                                msg=u'找到了！！'
                                if len(self.sprites) == len(self.card_list):
                                    msg = u'成功!'+ u'恭喜你找到全部神秘符号，用时：'+dur_time
                                    drawp = 'hh'
                            else:
                                msg =  u'没有找到'
                                pygame.time.wait(WAITING_TIME)
                                self.sprites.remove(opened_cards)
                            opened_cards = []
                        self.drawBackground()
                        self.drawCards()
                    else:
                        msg =  u"点击绿色的方块～"
        return True


if __name__ == '__main__':
    matchG = match_g()
    matchG.run()