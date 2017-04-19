#-*-coding=UTF-8-*-
import pygame
import random
import time
import sys
import string
import pygame, sys, random
from pygame.locals import *
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
darkGreen =     (0,166,0)
BLUE =          (0,0,240)
ORANGE = (255,140,0)

SCREEN_SIZE = [WINDOWWIDTH,WINDOWHEIGHT]
WIDTH = 100
HEIGHT = 100
WAITING_TIME = 1000

BGCOLOR = BLUE
TILECOLOR = darkGreen
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
msgColor = darkGreen

BASICFONTSIZE = 28
titleFontSize = 39
msgFontSize = 29

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = 0
YMARGIN = 0


pygame.mixer.init()
da_sound = pygame.mixer.Sound("da.wav")
di_sound = pygame.mixer.Sound("di.wav")
bg_sound = pygame.mixer.Sound("plant.wav")
click_sound = pygame.mixer.Sound('click.wav')

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
pygame.init()
BASICFONT = pygame.font.Font('gkai00mp.ttf', BASICFONTSIZE)
titleFONT = pygame.font.Font('gkai00mp.ttf', titleFontSize)
msg_font = pygame.font.Font('gkai00mp.ttf', msgFontSize)
output_font = pygame.font.Font('Arial.ttf', 19)
time_font = pygame.font.Font('Arial.ttf', 19)

FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption(u'伏羲')

DISPLAYSURF.fill(WHITE)
#pygame.draw.circle(screen,THECOLORS['blue'],[100,100],30,2)
background = pygame.Surface(SCREEN_SIZE)
background.fill([0,0,255])
start0 = pygame.image.load("start0.jpeg").convert_alpha()

DISPLAYSURF.blit(background,(0,0))
DISPLAYSURF.blit(start0,(0,0))

def bgSoundPlay():
    pygame.mixer.init()
    bg_sound = pygame.mixer.Sound("plant.wav")
    bg_sound.play(loops=3)

def makeText(text, color, bgcolor, top, left,fontSize=titleFONT):
    # create the Surface and Rect objects for some text.
    textSurf = fontSize.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

# Store the option buttons and their rectangles in OPTIONS.
global dur_time
dur_time = '0:0:0'
game1_SURF, game1_RECT = makeText(u'伏羲的启示', TEXTCOLOR, TILECOLOR, WINDOWWIDTH*0.1, 20)
game2_SURF, game2_RECT = makeText(u'神奇的八卦', TEXTCOLOR, TILECOLOR, WINDOWWIDTH*0.1, 80)
game3_SURF, game3_RECT = makeText(u'8421', TEXTCOLOR, TILECOLOR, WINDOWWIDTH*0.1, 140)
game4_SURF, game4_RECT = makeText(u'摩尔斯密码', TEXTCOLOR, TILECOLOR, WINDOWWIDTH*0.1, 200)
return_SURF, return_RECT = makeText(u'退出', TEXTCOLOR, msgColor, WINDOWWIDTH - 140, WINDOWHEIGHT - 160,fontSize=BASICFONT)
help_SURF, help_RECT = makeText(u'帮助', TEXTCOLOR, msgColor, WINDOWWIDTH - 140, WINDOWHEIGHT - 120,fontSize=BASICFONT)
RESET_SURF, RESET_RECT = makeText(u'设置', TEXTCOLOR, msgColor, WINDOWWIDTH - 140, WINDOWHEIGHT - 90,fontSize=BASICFONT)
NEW_SURF, NEW_RECT = makeText(u'新游戏', TEXTCOLOR, msgColor, WINDOWWIDTH - 140, WINDOWHEIGHT - 60,fontSize=BASICFONT)
SOLVE_SURF, SOLVE_RECT = makeText(u'破解', TEXTCOLOR, msgColor, WINDOWWIDTH - 140, WINDOWHEIGHT - 30,fontSize=BASICFONT)
next_SURF, next_RECT = makeText(u'继续', TEXTCOLOR, msgColor, 100, 0,fontSize=BASICFONT)
exit_SURF, exit_RECT = makeText(u'返回', TEXTCOLOR, msgColor, 200, 0,fontSize=BASICFONT)
time_SURF, time_RECT = makeText(u'用时：' + dur_time, TEXTCOLOR, ORANGE, 0, 50,fontSize=BASICFONT)

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


'''class background(pygame.sprite.Sprite):
    def __init__(self,filename,inittial_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect  = self.image.get_rect()
        self.rect.bottomright = inittial_position'''


def start_board():
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption(u'伏羲')

    DISPLAYSURF.fill(WHITE)
    # pygame.draw.circle(screen,THECOLORS['blue'],[100,100],30,2)
    background = pygame.Surface(SCREEN_SIZE)
    background.fill([0, 0, 255])
    start0 = pygame.image.load("start0.jpeg").convert_alpha()
    DISPLAYSURF.blit(background, (0, 0))
    DISPLAYSURF.blit(start0, (0, 0))
    DISPLAYSURF.blit(game1_SURF, game1_RECT)
    DISPLAYSURF.blit(game2_SURF, game2_RECT)
    DISPLAYSURF.blit(game3_SURF, game3_RECT)
    DISPLAYSURF.blit(game4_SURF, game4_RECT)

    pygame.display.flip()
    pygame.display.update()


def showHwnd(cardSize='500x450',filePath = './h2.gif'):
    top = Tkinter.Tk()
    top.title(u'知识卡片')
    top.geometry(cardSize)
    top.resizable(width=True, height=True)

    imgFile = filePath
    img = Tkinter.PhotoImage(file=imgFile)
    label1 = Tkinter.Label(top, image=img)
    label1.grid(column=0, row=0)
    top.mainloop()

start_board()
rank = 2


############################################      morseGame
class morseG(object):
    def __init__(self):

        self.input_SURF, self.input_RECT = makeText(u'输入:', TEXTCOLOR, msgColor, 100, WINDOWHEIGHT - 400)
        self.output_SURF, self.output_RECT = makeText(u'输出:', TEXTCOLOR, msgColor, 100, WINDOWHEIGHT - 350)

        self.translate_SURF, self.translate_RECT = makeText(u'翻译', TEXTCOLOR, msgColor, 150, WINDOWHEIGHT - 200)
        self.play_SURF, self.play_RECT = makeText(u'播放', TEXTCOLOR, msgColor, 300, WINDOWHEIGHT - 200)
        self.reset_SURF, self.reset_RECT = makeText(u'清空', TEXTCOLOR, msgColor, 450, WINDOWHEIGHT - 200)

        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption(u'摩尔斯密码')

        self.DISPLAYSURF.fill(WHITE)
        self.background = pygame.Surface([800, 600])
        self.background.fill(BGCOLOR)
        self.DISPLAYSURF.blit(self.background, (0, 0))
        pygame.display.update()

    #global input_SURF, input_RECT, output_SURF, output_RECT, translate_SURF, translate_RECT, play_SURF, play_RECT, pause_SURF, pause_RECT, reset_SURF, reset_RECT, exit1_SURF, exit1_RECT, help_SURF, help_RECT, return_SURF, return_RECT
    def bgSoundPlay(self):
        pygame.mixer.init()
        bg_sound = pygame.mixer.Sound("plant.wav")
        bg_sound.play(loops=3)

    def drawboard(self,msg = 'help cards',input_='',output_= ''):
        global input_SURF, input_RECT, output_SURF, output_RECT, translate_SURF, translate_RECT, play_SURF, play_RECT, pause_SURF, pause_RECT, reset_SURF, reset_RECT, exit1_SURF, exit1_RECT, help_SURF, help_RECT, return_SURF, return_RECT
        if msg:
            message_SURF,message_RECT = makeText(msg,MESSAGECOLOR, BGCOLOR, 5, 5,fontSize=msg_font)
            self.DISPLAYSURF.blit(message_SURF,message_RECT)
        if input_:
            self.input_SURF,self.input_RECT = makeText(input_,MESSAGECOLOR, BGCOLOR, 200, WINDOWHEIGHT - 390,fontSize=msg_font)
            self.DISPLAYSURF.blit(self.input_SURF,self.input_RECT)
        if output_:
            self.output_SURF,self.output_RECT = makeText(output_,MESSAGECOLOR, BGCOLOR, 200, WINDOWHEIGHT - 334,fontSize=output_font)
            self.DISPLAYSURF.blit(self.output_SURF,self.output_RECT)

        self.DISPLAYSURF.blit(self.translate_SURF, self.translate_RECT)
        self.DISPLAYSURF.blit(self.play_SURF, self.play_RECT)
        self.DISPLAYSURF.blit(self.reset_SURF, self.reset_RECT)

        self.DISPLAYSURF.blit(self.input_SURF, self.input_RECT)
        self.DISPLAYSURF.blit(self.output_SURF, self.output_RECT)

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
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.clicked = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.translate_RECT.collidepoint(self.clicked):
                    if not output_txt:
                        output_txt = self.translateChars(input_txt)
                    elif not input_txt:
                        input_txt = self.translateMorse(output_txt)
                        # self.morseplay(output_txt)
                elif self.play_RECT.collidepoint(self.clicked):
                    output_txt = self.translateChars(input_txt)
                    self.morseplay(output_txt)
                elif self.reset_RECT.collidepoint(self.clicked):
                    # self.morseplay(output_txt)
                    flag = 1
                    output_txt = ' ' * 100
                    input_txt = ' ' * 100
                elif return_RECT.collidepoint(self.clicked):
                    # print output_txt
                    return
                elif help_RECT.collidepoint(self.clicked):
                    # print output_txt
                    showHwnd()
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

###################################################      slideGame
class slide_g(object):
    def __init__(self,BOARDHEIGHT=2,BOARDWIDTH=2):
        self.bw = BOARDWIDTH
        self.bh = BOARDHEIGHT
        self.XMARGIN = int((WINDOWWIDTH - (TILESIZE * self.bw + (self.bw - 1))) / 2)
        self.YMARGIN = int((WINDOWHEIGHT - (TILESIZE * self.bh + (self.bh - 1))) / 2)

    def main(self):
        global msg,FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, next_SURF, next_RECT,return_SURF, return_RECT, help_SURF, help_RECT

        mainBoard, solutionSeq = self.generateNewPuzzle(2)
        SOLVEDBOARD = self.getStartingBoard() # a solved board is the same as the board in a start state.
        allMoves = [] # list of moves made from the solved configuration
        msg = u'点击数字或按下键盘的上下左右键滑动数字'
        while True: # main game loop
            slideTo = None # the direction, if any, a tile should slide
             # contains the message to show in the upper left corner.
            drawp = ''
            if mainBoard == SOLVEDBOARD:
                msg = u'成功!'
                #print u'成功',self.bw
                drawp = 'true'
                if self.bw == 4:
                    msg = u'恭喜你，通过第二关'
                    drawp = ''
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        self.clickxy = event.pos
                    if event.type == MOUSEBUTTONUP:
                        if next_RECT.collidepoint(event.pos):
                            rank = self.bw + 1
                            newgame = slide_g(BOARDWIDTH=rank,BOARDHEIGHT=rank)
                            if rank < 5:
                                newgame.main()
                            else:
                                msg = u'恭喜你，通过第二关'
                        elif exit_RECT.collidepoint(event.pos):
                            return
                #return True
            self.drawBoard(mainBoard, msg,drawp)
            self.checkForQuit()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    spotx, spoty = self.getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                    if (spotx, spoty) == (None, None):
                        # check if the user clicked on an option button
                        if RESET_RECT.collidepoint(event.pos):
                            self.resetAnimation(mainBoard, allMoves) # clicked on Reset button
                            allMoves = []
                        elif NEW_RECT.collidepoint(event.pos):
                            mainBoard, solutionSeq = self.generateNewPuzzle(10) # clicked on New Game button
                            allMoves = []
                        elif SOLVE_RECT.collidepoint(event.pos):
                            self.resetAnimation(mainBoard, solutionSeq + allMoves) # clicked on Solve button
                            allMoves = []
                        elif exit_RECT.collidepoint(event.pos):
                            return
                        elif return_RECT.collidepoint(event.pos):
                            return
                        elif help_RECT.collidepoint(event.pos):
                            showHwnd(cardSize='200x200',filePath='./8421.gif')
                            if self.bw == 2:
                                msg = u'01(1) < 10(2) < 11(3)'
                            elif self.bw == 3:
                                msg = '001 < 010 < 011 < 100 < 101 < 110 < 111'
                    else:
                        # check if the clicked tile was next to the blank spot
                        blankx, blanky = self.getBlankPosition(mainBoard)
                        if spotx == blankx + 1 and spoty == blanky:
                            slideTo = LEFT
                        elif spotx == blankx - 1 and spoty == blanky:
                            slideTo = RIGHT
                        elif spotx == blankx and spoty == blanky + 1:
                            slideTo = UP
                        elif spotx == blankx and spoty == blanky - 1:
                            slideTo = DOWN

                elif event.type == KEYUP:
                    # check if the user pressed a key to slide a tile
                    if event.key in (K_LEFT, K_a) and self.isValidMove(mainBoard, LEFT):
                        slideTo = LEFT
                    elif event.key in (K_RIGHT, K_d) and self.isValidMove(mainBoard, RIGHT):
                        slideTo = RIGHT
                    elif event.key in (K_UP, K_w) and self.isValidMove(mainBoard, UP):
                        slideTo = UP
                    elif event.key in (K_DOWN, K_s) and self.isValidMove(mainBoard, DOWN):
                        slideTo = DOWN
            if slideTo:
                self.slideAnimation(mainBoard, slideTo, u'点击数字或按上下左右键移动数字', 8) # show slide on screen
                self.makeMove(mainBoard, slideTo)
                allMoves.append(slideTo) # record the slide
            pygame.display.update()
            FPSCLOCK.tick(FPS)

    def terminate(self):
        return

    def checkForQuit(self):
        for event in pygame.event.get(QUIT): # get all the QUIT events
            self.terminate() # terminate if any QUIT events are present
        for event in pygame.event.get(KEYUP): # get all the KEYUP events
            if event.key == K_ESCAPE:
                self.terminate() # terminate if the KEYUP event was for the Esc key
            pygame.event.post(event) # put the other KEYUP event objects back

    def format_bin(self,number_, bw):
        bin_num = bin(number_).replace('0b', '')
        if len(bin_num) != bw:
            bin_num = (bw - len(bin_num)) * '0' + bin_num
        return bin_num
    def getStartingBoard(self):
        # Return a board data structure with tiles in the solved state.
        # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
        # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
        counter = 1
        board = []
        counter1 = self.format_bin(counter,self.bw)
        for x in range(self.bw):
            column = []
            for y in range(self.bh):
                column.append(counter1)
                counter += self.bw
                counter1 = self.format_bin(counter, self.bw)
            board.append(column)
            counter -= self.bw * (self.bh - 1) + self.bw - 1
            counter1 = self.format_bin(counter, self.bw)
        board[self.bw-1][self.bh-1] = BLANK
        print board
        return board

    def getBlankPosition(self,board):
        # Return the x and y of board coordinates of the blank space.
        for x in range(self.bw):
            for y in range(self.bh):
                if board[x][y] == BLANK:
                    return (x, y)

    def makeMove(self,board, move):
        # This function does not check if the move is valid.
        blankx, blanky = self.getBlankPosition(board)
        if move == UP:
            board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
        elif move == DOWN:
            board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
        elif move == LEFT:
            board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
        elif move == RIGHT:
            board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]

    def isValidMove(self,board, move):
        blankx, blanky = self.getBlankPosition(board)
        return (move == UP and blanky != len(board[0]) - 1) or \
               (move == DOWN and blanky != 0) or \
               (move == LEFT and blankx != len(board) - 1) or \
               (move == RIGHT and blankx != 0)

    def getRandomMove(self,board, lastMove=None):
        # start with a full list of all four moves
        validMoves = [UP, DOWN, LEFT, RIGHT]
        # remove moves from the list as they are disqualified
        if lastMove == UP or not self.isValidMove(board, DOWN):
            validMoves.remove(DOWN)
        if lastMove == DOWN or not self.isValidMove(board, UP):
            validMoves.remove(UP)
        if lastMove == LEFT or not self.isValidMove(board, RIGHT):
            validMoves.remove(RIGHT)
        if lastMove == RIGHT or not self.isValidMove(board, LEFT):
            validMoves.remove(LEFT)

        # return a random move from the list of remaining moves
        return random.choice(validMoves)

    def getLeftTopOfTile(self,tileX, tileY):
        left = self.XMARGIN + (tileX * TILESIZE) + (tileX - 1)
        top = self.YMARGIN + (tileY * TILESIZE) + (tileY - 1)
        return (left, top)

    def getSpotClicked(self,board, x, y):
        # from the x & y pixel coordinates, get the x & y board coordinates
        for tileX in range(len(board)):
            for tileY in range(len(board[0])):
                left, top = self.getLeftTopOfTile(tileX, tileY)
                tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
                if tileRect.collidepoint(x, y):
                    return (tileX, tileY)
        return (None, None)


    def drawTile(self,tilex, tiley, number, adjx=0, adjy=0):
        # draw a tile at board coordinates tilex and tiley, optionally a few
        # pixels over (determined by adjx and adjy)
        left, top = self.getLeftTopOfTile(tilex, tiley)
        pygame.draw.rect(DISPLAYSURF, GREEN, (left + adjx, top + adjy, TILESIZE, TILESIZE))
        textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
        textRect = textSurf.get_rect()
        textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
        DISPLAYSURF.blit(textSurf, textRect)

    def drawBoard(self,board, message,drawp=''):
        DISPLAYSURF.fill(BGCOLOR)
        if message:
            textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
            DISPLAYSURF.blit(textSurf, textRect)

        for tilex in range(len(board)):
            for tiley in range(len(board[0])):
                if board[tilex][tiley]:
                    self.drawTile(tilex, tiley, board[tilex][tiley])

        left, top = self.getLeftTopOfTile(0, 0)
        width = self.bw * TILESIZE
        height = self.bh * TILESIZE
        pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

        DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
        DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
        DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)
        DISPLAYSURF.blit(return_SURF, return_RECT)
        DISPLAYSURF.blit(help_SURF, help_RECT)
        if drawp:
            DISPLAYSURF.blit(next_SURF, next_RECT)
            DISPLAYSURF.blit(exit_SURF, exit_RECT)


    def slideAnimation(self,board, direction, message, animationSpeed):
        # Note: This function does not check if the move is valid.

        blankx, blanky = self.getBlankPosition(board)
        if direction == UP:
            movex = blankx
            movey = blanky + 1
        elif direction == DOWN:
            movex = blankx
            movey = blanky - 1
        elif direction == LEFT:
            movex = blankx + 1
            movey = blanky
        elif direction == RIGHT:
            movex = blankx - 1
            movey = blanky

        # prepare the base surface
        self.drawBoard(board, message)
        baseSurf = DISPLAYSURF.copy()
        # draw a blank space over the moving tile on the baseSurf Surface.
        moveLeft, moveTop = self.getLeftTopOfTile(movex, movey)
        pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

        for i in range(0, TILESIZE, animationSpeed):
            # animate the tile sliding over
            self.checkForQuit()
            DISPLAYSURF.blit(baseSurf, (0, 0))
            if direction == UP:
                self.drawTile(movex, movey, board[movex][movey], 0, -i)
            if direction == DOWN:
                self.drawTile(movex, movey, board[movex][movey], 0, i)
            if direction == LEFT:
                self.drawTile(movex, movey, board[movex][movey], -i, 0)
            if direction == RIGHT:
                self.drawTile(movex, movey, board[movex][movey], i, 0)

            pygame.display.update()
            FPSCLOCK.tick(FPS)


    def generateNewPuzzle(self,numSlides):
        # From a starting configuration, make numSlides number of moves (and
        # animate these moves).
        sequence = []
        board = self.getStartingBoard()
        self.drawBoard(board, '')
        pygame.display.update()
        pygame.time.wait(500) # pause 500 milliseconds for effect
        lastMove = None
        for i in range(numSlides):
            move = self.getRandomMove(board, lastMove)
            self.slideAnimation(board, move, u'游戏初始化......', animationSpeed=int(TILESIZE / 3))
            self.makeMove(board, move)
            sequence.append(move)
            lastMove = move
        return (board, sequence)

    def resetAnimation(self,board, allMoves):
        # make all of the moves in allMoves in reverse.
        revAllMoves = allMoves[:] # gets a copy of the list
        revAllMoves.reverse()
        for move in revAllMoves:
            if move == UP:
                oppositeMove = DOWN
            elif move == DOWN:
                oppositeMove = UP
            elif move == RIGHT:
                oppositeMove = LEFT
            elif move == LEFT:
                oppositeMove = RIGHT
            self.slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 2))
            self.makeMove(board, oppositeMove)

#######################################################  matchgame    #################
class background(pygame.sprite.Sprite):
    def __init__(self,filename,inittial_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect  = self.image.get_rect()
        self.rect.bottomright = inittial_position


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
        global dur_time,time_RECT,time_SURF
        dur_time = durTime
        #print dur_time
        dur_time = str(int(round(durTime/3600,0)))+':'+str(int(round(durTime/60,0)))+':'+str(int(round(durTime%60,0)))
        #print dur_time
        if message:
            textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5,fontSize=msg_font)
            self.mbackground.blit(textSurf, textRect)
        if drawp:
            self.mbackground.blit(next_SURF, next_RECT)
            self.mbackground.blit(return_SURF, return_RECT)
        time_SURF, time_RECT = makeText(u'用时：' + dur_time, TEXTCOLOR, ORANGE, 0, 50, fontSize=BASICFONT)
        self.mbackground.blit(time_SURF, time_RECT)
        DISPLAYSURF.blit(self.mbackground, (0, 0))
        pygame.display.flip()


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
        self.mbackground.blit(return_SURF, return_RECT)
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
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play(loops=1)
                #print event.pos
                self.clicked = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if help_RECT.collidepoint(event.pos):
                    #msg='help info'
                    showHwnd(cardSize='620x300',filePath = './h1.gif')
                elif SOLVE_RECT.collidepoint(event.pos):
                    msg = 'solve info'
                elif return_RECT.collidepoint(event.pos):
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
                start_board()
            elif game3_RECT.collidepoint(event.pos):
                bg_sound.stop()
                slide = slide_g(BOARDHEIGHT=rank, BOARDWIDTH=rank)
                slide.main()
                start_board()
            elif game4_RECT.collidepoint(event.pos):
                bg_sound.stop()
                morse_g = morseG()
                morse_g.main()
                start_board()
