# encoding: utf-8
import pygame
import sys

pygame.init()

en_words = 'hello world!'
zh_words = u"世界， 你好"
#my_en_font = pygame.font.Font('FreeMono.ttf', 64)
my_font = pygame.font.Font('gkai00mp.ttf', 64)
#my_font_wd = pygame.font.Font('wingding.ttf', 64)
#en_suface = my_en_font.render(en_words, True, (0, 0, 0))
ch_suface = my_font.render(zh_words, True, (0, 0, 0))
#wd_suface = my_font_wd.render(zh_words, True, (0, 0, 0))
#pygame.image.save(en_suface, 'en_hello.png')
screen = pygame.display.set_mode([600,500])
screen.fill([255,255,255])
screen.blit(ch_suface,(100,100))
pygame.display.flip()
pygame.display.update()
running  = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            print clicked
#pygame.image.save(ch_suface, 'ch_hello.png')
#pygame.image.save(wd_suface, 'wd_hello.png')