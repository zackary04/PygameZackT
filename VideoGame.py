#Jumpy and the Jumpy Bunch Pycode
#Official Update 4.7.20
#Error has occurred with platforms
#Game over appears, albeit very very briefly

import pygame, sys

from pygame.locals import *

from enum import Enum

from pygame import mixer

import os, math

import random
import time

#Initialize pygame
pygame.init()
miny = 313
pygame.time.set_timer(USEREVENT + 1, 7000)  

theFont=pygame.font.Font(None,72)
theTime=0 #pygame.time.get_ticks()
timeText=theFont.render(str(theTime), True,(255,255,255),(0,0,0))

W, H = 800, 447

#List of RGB Colors
PURPLE = 255, 0, 255
CYAN = 0, 255, 255
BLACK = 0, 0, 0
WHITE = 255, 255, 255
MAGENTA = 255, 0, 127

win = pygame.display.set_mode((W, H))

pygame.display.set_caption('Jumpy and the Jumpy Bunch')
icon = pygame.image.load('Pixel Mario.jpg')
pygame.display.set_icon(icon)

bg = pygame.image.load("resources/images/clouds.jpg")

#Background Sound
#mixer.music.load('Planet_Wisp.mp3')
#mixer.music.play(-1)

bgX = 0

bgX2 = bg.get_width()

clock = pygame.time.Clock()

#Added for main menu part
mainClock = pygame.time.Clock()

font = pygame.font.SysFont(None, 20)

def draw_text(text, font, color, surface, x, y):
   textobj = font.render(text, 1, color)
   textrect = textobj.get_rect()
   textrect.topleft = (x, y)
   surface.blit(textobj, textrect)

#Newly added, perhaps this will help choose our screens
def main():
   pygame.init()

   screen = pygame.display.set_mode((800, 600))
   #added for background
   BGscreen = pygame.image.load("Start_Menu_Image.jpg")
   game_state = GameState.TITLE

   while True:
       #added for background
       BGscreen.fill(BLACK)
       BGscreen.blit(BGscreen, (0, 0))


       if game_state == GameState.TITLE:
           game_state = title_screen()

       if game_state == GameState.NEWGAME:
           game_state = game_main()

       if game_state == GameState.QUIT:
           pygame.quit()
           return
#boop boo de boop


#This is our Title_Screen menu
def title_screen():
   click = False

   while True:

       win.fill((BLACK))
       draw_text('Welcome to Jumpy and the Jumpy Bunch!', font, (WHITE), win, 310, 20)
       draw_text("Click the top button to play, the middle one for options, or the bottom one "
                 "for the credits page.", font, (WHITE), win, 20, 40)
       draw_text("Press ESC to exit game or menus.", font, (WHITE), win, 20, 60)
       draw_text("Good luck and Have Fun!", font, (WHITE), win, 310, 410)

       mx, my = pygame.mouse.get_pos()
       #pass indicates if button has been clicked

       #First two numbers represent X and Y coordinates
       button_1 = pygame.Rect(50, 100, 200, 50)
       button_2 = pygame.Rect(50, 200, 200, 50)
       button_3 = pygame.Rect(50, 300, 200, 50)
       #This click should run the gameplay
       if button_1.collidepoint((mx, my)):
           if click:
               game_main() #The actual game code is listed under def game_main()
       #This click will run options menu
       if button_2.collidepoint((mx, my)):
           if click:
               Options()
       #This click will run the credits page menu
       if button_3.collidepoint((mx, my)):
           if click:
               Credits()

       #These are our buttons
       pygame.draw.rect(win, (CYAN), button_1)
       pygame.draw.rect(win, (PURPLE), button_2)
       pygame.draw.rect(win, (MAGENTA), button_3)

       click = False
       for event in pygame.event.get():
           if event.type == QUIT:
               pygame.quit()
               sys.exit()
           if event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                   pygame.quit()
                   sys.exit()
           if event.type == MOUSEBUTTONDOWN:
               if event.button == 1:
                   click = True

       pygame.display.update()
       mainClock.tick(60)

#When the button is clicked, this should initiate the credits now instead of just text
def Credits():
   running = True
   while running:
       win.fill((0, 0, 0))

       draw_text('Credits Menu', font, (255, 255, 255), win, 360, 20)
       draw_text("This is the credits page.", font, (255, 255, 255), win, 20, 40)
       draw_text("Massive shoutouts and kudos to the fellas who worked hard to make this game a "
                 "reality.", font, (255, 255, 255), win, 20, 60)
       draw_text("Special thanks to: Zackary T., Andre S., Robert C., and Mark M."
                 , font, (255, 255, 255), win, 20, 80)
       for event in pygame.event.get():
           if event.type == QUIT:
               pygame.quit()
               sys.exit()
           if event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                   running = False

       pygame.display.update()
       mainClock.tick(60)

#This will display info like controls
def Options():
   running = True
   while running:
       win.fill((0,0,0))

       draw_text('Options Menu', font, (255, 255, 255), win, 360, 20)
       draw_text("Controls: ", font, (255, 255, 255), win, 20, 40)
       draw_text("Press SPACE or Arrow Up to jump.", font, (255, 255, 255), win, 20, 60)
       draw_text("Press Arrow Down to slide. ", font, (255, 255, 255), win, 20, 80)
       draw_text("Instructions: ", font, (255, 255, 255), win, 20, 120)
       draw_text("Jump from platform to platform to avoid falling. "
                 "If you fall off, you will lose and be returned to the title screen."
                 , font, (255, 255, 255), win, 20, 140)
       for event in pygame.event.get():
           if event.type == QUIT:
               pygame.quit()
               sys.exit()
           if event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                   running = False

       pygame.display.update()
       mainClock.tick(60)


class player(object):
   run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8, 16)]

   jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1, 8)]

   slide = [pygame.image.load(os.path.join('images', 'S1.png')),
            pygame.image.load(os.path.join('images', 'S2.png')),
            pygame.image.load(os.path.join('images', 'S2.png')),
            pygame.image.load(os.path.join('images', 'S2.png')),
            pygame.image.load(os.path.join('images', 'S2.png')),
            pygame.image.load(os.path.join('images', 'S2.png')),
            pygame.image.load(os.path.join('images', 'S2.png')),
            pygame.image.load(os.path.join('images', 'S2.png')),
            pygame.image.load(os.path.join('images', 'S3.png')),
            pygame.image.load(os.path.join('images', 'S4.png')),
            pygame.image.load(os.path.join('images', 'S5.png'))]

   jumpList = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4,
               4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1,
               -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3,
               -3, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4]

   fallrate = -2

   def __init__(self, x, y, width, height):

       self.x = x

       self.y = y

       self.width = width

       self.height = height

       self.jumping = False

       self.sliding = False

       self.slideCount = 0

       self.jumpCount = 0

       self.runCount = 0

       self.slideUp = False

   def draw(self, win):

       if self.jumping:

           self.y -= self.jumpList[self.jumpCount] * 1.2

           if self.y >= miny:
               self.y = miny

           win.blit(self.jump[self.jumpCount // 18], (self.x, self.y))

           self.jumpCount += 1

           if self.y == miny:
               self.jumCount = 111

           if self.jumpCount > 108:
               self.jumpCount = 0

               self.jumping = False

               self.runCount = 0

       elif self.sliding or self.slideUp:

           if self.slideCount < 20:
               self.y += 1

           elif self.slideCount == 80:
               self.y -= 19
               self.sliding = False
               self.slideUp = True

           if self.slideCount >= 110:
               self.slideCount = 0
               self.slideUp = False
               self.runCount = 0

           win.blit(self.slide[self.slideCount // 10], (self.x, self.y))

           self.slideCount += 1



       else:
           if self.runCount > 42:
               self.runCount = 0

           if self.y < miny:
               self.y -= self.fallrate

           win.blit(self.run[self.runCount // 6], (self.x, self.y))

           self.runCount += 1

class platform(object):
   plat = pygame.image.load("resources/images/platform.jpg")

   def __init__(self, x, y, width, height):
       self.x = x

       self.y = y

       self.width = width

       self.height = height

   def draw(self, win):
       win.blit(self.plat, (self.x, self.y))

#Here is where the two updates begin to diverge from likeness
def redrawWindow():
    win.blit(bg, (bgX, 0))  # draws our first bg image
    win.blit(bg, (bgX2, 0))  # draws the seconf bg image
    
    for p in platforms:
        p.draw(win)
    runner.draw(win)
    win.blit(timeText,(0,0))
    pygame.display.update()  # updates the screen



platforms= [platform(810, 313, 64, 64)]
runner = player(200, 313, 64, 64)
def game_main():
   global bgX, bgX2,platforms, runner, miny,theFont, theTime,timeText

   run = True

   speed = 100

   runner = player(200, 313, 64, 64)

   platforms = [platform(810, 313, 64, 64)]
   pygame.time.set_timer(USEREVENT + 3, 100)

   pygame.time.set_timer(USEREVENT + 2, 2500)  # Will trigger every 2 - 3.5 s
   timer=0
   signal = 0
   theTime=0

   while run:
       timer=round(timer,3)
       stringTime=str(timer)+' sec'
       timeText=theFont.render(stringTime, True,(255,255,255),(0,0,0))


       redrawWindow() 
       bgX -= 1.4

       bgX2 -= 1.4

       for p in platforms:

           p.x -= 1.4

           if p.x < p.width * -1:  # If our obstacle is off the screen we will remove it

               platforms.pop(platforms.index(p))  # their code

       if platforms[0].x <= 200 and platforms[0].x >= 0:

           miny = platforms[0].y - 50

       else:

           miny = 400

       if signal == 1 and runner.jumping == False and runner.sliding == False and runner.slideUp == False:

           if runner.y > miny + 10:
               run = False

       if bgX < bg.get_width() * -1:
           bgX = bg.get_width()

       if bgX2 < bg.get_width() * -1:
           bgX2 = bg.get_width()

       keys = pygame.key.get_pressed()

       if keys[pygame.K_SPACE] or keys[pygame.K_UP]:  # If user hits space or up arrow key

           if not (runner.jumping):  # If we are not already jumping

               runner.jumping = True

       if keys[pygame.K_DOWN]:  # If user hits down arrow key

           if not (runner.sliding):  # If we are not already sliding

               runner.sliding = True

       # Because we have a starter file this is all we have to do to move our character.

       # The physics and math behind the movement has been coded for you.

       for event in pygame.event.get():

           if event.type == pygame.QUIT:
               run = False

               pygame.quit()

               quit()

           if event.type == USEREVENT + 1:  # Checks if timer goes off

               signal = 1  # Increases speed

           if event.type == USEREVENT + 2:
               newplat = platform(810, random.randint(math.floor(runner.y - 2), 400), 64, 64)

               platforms.append(newplat)
           if event.type== USEREVENT + 3:
               timer=timer+.1

       clock.tick(speed)
       



   win.blit(bg, (bgX, 0))  # draws our first bg image
   win.blit(bg, (bgX2, 0))  # draws the seconf bg image
    
   for p in platforms:
       p.draw(win)
   runner.draw(win)
   win.blit(pygame.image.load("resources/images/gameOver.jpg"), (300,200))
   win.blit(timeText,(0,0))
   pygame.display.update()  # updates the screen
   time.sleep(2) #sleep for three seconds

#New, this may be the case for our screen transitions
class GameState(Enum):
   QUIT = -1
   TITLE = 0
   NEWGAME = 1

title_screen()
