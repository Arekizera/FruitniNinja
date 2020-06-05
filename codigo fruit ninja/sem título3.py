# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 14:32:51 2020

@author: rafa1
"""
import pygame, sys
import random
import os
# Setup pygame/window ---------------------------------------- #

from pygame.locals import *
pygame.init()
game_folder=os.path.dirname(__file__)
image_folder=os.path.join(game_folder,"Images")
fruit_folder=os.path.join(image_folder,"Fruits")
ui_folder=os.path.join(image_folder,"UI")
explosion_folder=os.path.join(image_folder,"exp")
background_folder=os.path.join(image_folder,"Backround")
music_folder=os.path.join(game_folder,"Music")
length = 1300 #1500
hight = 700 #900
size = (length,hight)
screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
pygame.display.set_caption("Fruit Ninja")
cut_sound = pygame.mixer.Sound(os.path.join(music_folder,"cut.wav"))
apple_sound = pygame.mixer.Sound(os.path.join(music_folder,"apple.wav"))
orange_sound = pygame.mixer.Sound(os.path.join(music_folder,"orange.wav"))
banna_sound = pygame.mixer.Sound(os.path.join(music_folder,"banna.wav"))
bomb_sound = pygame.mixer.Sound(os.path.join(music_folder,"bomb.wav"))
start_sound = pygame.mixer.Sound(os.path.join(music_folder,"start.wav"))
end_sound = pygame.mixer.Sound(os.path.join(music_folder,"end.wav"))
check_sound = pygame.mixer.Sound(os.path.join(music_folder,"check.wav"))
uncheck_sound = pygame.mixer.Sound(os.path.join(music_folder,"uncheck.wav"))
musicas=True
musica_i=True
carryOn = True
time = 0
mainClock = pygame.time.Clock()
#pygame.font.init()
font = pygame.font.Font(None, 50)
pygame.display.set_caption('game base')
 
font = pygame.font.SysFont(None, 20)
 
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
 
click = False
 
def main_menu():
    musica_i=True
    while True:
        
        screen.fill((0,0,0))
        if musica_i:
            pygame.mixer.Sound.play(end_sound)
            musica_i=False
        background = pygame.image.load(os.path.join(background_folder,"startscreen.jpg")).convert()
        screen.fill([0,0,0])
        screen.blit(background, [0,0])
        draw_text('main menu', font, (255, 255, 255), screen, 20, 20)
 
        mx, my = pygame.mouse.get_pos()
 
        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
 
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

def game():
    musica_i=True
    running = True
    while running:
        class Player(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.Surface((0,0))
                self.image.fill([211,211,211])
                self.rect = self.image.get_rect()
                self.rect.x = 0
                self.rect.y = 0
            def update(self):
        #--------------Restrict Movment around edges-----------------
                pos=pygame.mouse.get_pos()
                mouse=pygame.mouse.get_pressed()
                self.rect.x=pos[0]
                self.rect.y=pos[1]
                if mouse[0] == 1:
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                else:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
                
        class Apple(pygame.sprite.Sprite):
            def __init__(self,start):
                pygame.sprite.Sprite.__init__(self)
                self.image=pygame.image.load(os.path.join(fruit_folder,"greenapple.png")).convert_alpha()
                self.rect=self.image.get_rect()
                self.rect.x=random.randint(0,length-150)
                self.rect.y=random.randint(hight,hight+4000)
                self.time=time
                self.const=1
                self.error=0
                self.p=0
                self.kp=0.2
                self.hight=0
                gvars.fruit_count+=1
                self.start=start
                self.angle=0
            def update(self):
                pos=pygame.mouse.get_pos()
                mouse=pygame.mouse.get_pressed()
                if time ==self.start:
                    self.time=time+50
                    self.const=1
                    self.hight=110
                elif time<self.start:
                    self.time=time
                if self.time>time:
                    self.error=self.hight-self.rect.y
                    self.p = self.error*self.kp
                    self.rect.y+=init(self.p)
                elif self.time+5<time and self.rect.y<hight:
                    self.const+=0.4
                    self.rect.y+=int(2*self.const)
                
                if self.rect.y>hight+200:
                    gvars.fruit_count-=1
                    self.kill()
                if mouse[0]==1 and self.rect.collidepoint(pos[0],pos[1]):
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                    gvars.fruit_count-=1
                    self.kill()
                    self.Sliced()
                    gvars.score+=1
                else:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
        
        
        
        
            def Sliced(self):
                pygame.mixer.Sound.play(apple_sound)
                applecut1=AppleCut1(self.rect.x,self.rect.y,self.const)
                all_sprites.add(applecut1)
                applecut2=AppleCut2(self.rect.x,self.rect.y,self.const)
                all_sprites.add(applecut2)
        
        class AppleCut1 (pygame.sprite.Sprite):
            def __init__(self,x,y,velocity):
                pygame. sprite. Sprite. __init__(self)
                self.image=pygame.image.load(os.path.join(fruit_folder,"greenapplecut1.png")).convert_alpha()
                self.rect=self.image.get_rect ()
                self.rect.x=x-80
                self.rect.y=y
                self.const=velocity
            def update (self):
                self.const+=0.4
                self.rect.y+=int(2*self.const)
                if self.rect.y>hight+200:
                    self.kill()
        class AppleCut2 (pygame.sprite.Sprite):
            def __init__(self,x,y,velocity):
                pygame.sprite.Sprite.__init__(self)
                self.image=pygame.image.load(os.path.join(fruit_folder,"greenapplecut2.png")).convert_alpha()
                self.rect=self.image.get_rect ()
                self.rect.x=x+80
                self.rect.y=y
                self.const=velocity
            def update(self):
                self.const+=0.4
                self.rect.y+=int(2*self.const)
                if self.rect.y>hight+200:
                    self.kill()
        
        class Banna(pygame.sprite. Sprite):
            def __init__(self,start):
                pygame.sprite.Sprite.__init__(self)
                self.image=pygame.image.load (os.path.join(fruit_folder, "banna.png")).convert_alpha()
                self.rect=self.image.get_rect()
                self.rect.x=random.randint(0,length-150)
                self.rect.y=random.randint(hight,hight+4000)
                self.time=time
                self.const=1
                self.error=0
                self.p=0
                self.kp=0.2
                self.hight=0
                gvars.fruit_count+=1
                self.start=start
            def update(self):
                pos=pygame.mouse.get_pos()
                mouse=pygame.mouse.get_pressed()
                if time==self.start:
                    self.time=time+50
                    self.const=1
                    self.hight=110
                elif time<self.start:
                    self.time=time
                if self.time>time:
                    self.error=self.hight-self.rect.y
                    self.p=self.error*self.kp
                    self.rect.y+=int(self.p)
                elif self.time+5<time and self.rect.y<hight:
                    self.const+=0.4
                    self.rect.y+=int(2*self.const)
                if self.rect.y>hight+200:
                    gvars.fruit_count-=1
                    self.kill() 
                if mouse[0]==1 and self.rect.collidepoint(pos[0],pos[1]):
                    gvars.score+=1
                    gvars.fruit_count-=1
                    self.kill()
                    self.Sliced()
        
            def Sliced(self):
                pygame.mixer.Sound.play(banna_sound)
                bannacut1=BannaCut1(self.rect.x,self.rect.y,self.const)
                all_sprites.add(bannacut1)
                bannacut2=BannaCut2(self.rect.x,self.rect.y,self.const)
                all_sprites.add(bannacut2)
        
        class BannaCut1(pygame.sprite.Sprite):
            def __init__(self,x,y,velocity):
                pygame.sprite.Sprite.__init__(self)
                self.image=pygame.image.load(os.path.join(fruit_folder,"bannacut1.png")).convert_alpha()
                self.rect=self.image.get_rect()
                self.rect.x=x-150
                self.rect.y=y
                self.const=velocity
            def update(self):
                self.const+=0.4
                self.rect.y+=int(2*self.const)
                if self.rect.y>hight+200:
                    self.kill()
        
        
        class BannaCut2(pygame.sprite.Sprite):
            def __init__(self,x,y,velocity):
                pygame.sprite.Sprite.__init__(self)
                self.image=pygame.image.load(os.path.join(fruit_folder,"bannacut2.png")).convert_alpha()
                self.rect=self.image.get_rect()
                self.rect.x=x-150
                self.rect.y=y
                self.const=velocity
            def update(self):
                self.const+=0.4
                self.rect.y+=int(2*self.const)
                if self.rect.y>hight+200:
                    self.kill()
        
        class Pineapple(pygame.sprite.Sprite):
            def __init__(self,start):
                pygame.sprite.Sprite.__init__(self)
                self.image=pygame.image.load(os.path.join(fruit_folder,"pineapple.png")).convert_alpha()
                self.rect=self.image.get_rect()
                self.rect.x=random.randint(0,lenght-150)
                self.rect.y=random.randint(hight,hight+4000)
                self.time=time
                self.const=1
                self.error=0
                self.p=0
                self.kp=0.2
                self.hight=0
                gvars.fruit_count+=1
                self.start=start
            def update(self):
                pos=pygame.mouse.get_pos()
                mouse=pygame.mouse.get_pressed()
                if time==self.start:
                    self.time=time+50
                    self.const=1
                    self.hight=110
                elif time<self.start:
                    self.time=time
                if self.time>time:
                    self.error=self.hight-self.rect.y
                    self.p=self.error*self.kp
                    self.rect.y+=int(self.p)
                elif self.time+5<time and self.rect.y<hight:
                    self.const+=0.4
                    self.rect.y+=int(2*self.const)
        
                if self.rect.y>hight+200:
                    gvars.fruit_count-=1
                    self.kill()
                if mouse[0]==1 and self.rect.collidepoint(pos[0],pos[1]):
                    gvars.fruit_counter-=1
                    gvars.score+=1
                    self.kill()
                    self.Sliced()
                
                def Sliced(self):
                    pygame.mixer.Sound.play(cut_sound)
                    pineapplecut1=PineappleCut1(self.rect.x,self.rect.y,self.const)
                    all_sprites.add(pineapplecut1)
                    pineapplecut2=PineappleCut2(self.rect.x,self.rect.y,self.const)
                    all_sprites.add(pineapplecut2)
        
        class PineappleCut1(pygame.sprite.Sprite):
            def __init__(self,x,y,velocity):
                pygame.sprite.Sprite.__init__(self)
                self.image=pygame.image.load(os.path.join(fruit_folder,"pineapplecut1.png")).convert_alpha()
                self.rect=self.image.get_rect()
                self.rect.x=x-20
                self.rect.y=y-150
                self.const=velocity
            def update(self):
                self.const+=0.4
                self.rect.y+=int(2*self.const)
                if self.rect.y>hight+200:
                    self.kill()
        
        class PineappleCut2(pygame.sprite.Sprite):
            def __init__(self,x,y,velocity):
                pygame.sprite.Sprite.__init__(self)
                self.image=pygame.image.load(os.path.join(fruit_folder,"pineapplecut2.png")).convert_alpha()
                self.rect=self.image.get_rect()
                self.rect.x=x
                self.rect.y=y+150
                self.const=velocity
            def update(self):
                self.const+=0.4
                self.rect.y+=int(2*self.const)
                if self.rect.y>hight+200:
                    self.kill()
        
        class Radish(pygame.sprite.Sprite):
            def __init__(self,start):
                pygame.sprite.Sprite.__init__(self)
                self.image=pygame.image.load(os.path.join(fruit_folder,"radish.png")).convert_alpha()
                self.rect=self.image.get_rect()
                self.rect.x=random.randint(0,length-150)
                self.rect.y=random.randint(hight,hight+4000)
                self.time=time
                self.const=1
                self.error=0
                self.p=0
                self.kp=0.2
                self.hight=0
                gvars.fruit_count+=1
                self.start=start
            def update(self):
                pos=pygame.mouse.get_pos()
                mouse=pygame.mouse.get_pressed() 
                if time==self.start:
                    self.time=time+50
                    self.const=1
                    self.hight=110
                elif time<self.start:
                    self.time=time
                if self.time>time:
                    self.error=self.hight-self.rect.y
                    self.p=self.error*self.kp
                    #print("P:",int(self.p))
                    self.rect.y+=int(self.p)
                elif self.time+5<time and self.rect.y<hight:
                    self.const+=0.4
                    self.rect.y+=int(2*self.const)
                if self.rect.y>hight+200:
                    gvars.fruit_count-=1
                    self.kill()
                if mouse[0]==1 and self.rect.collidepoint(pos[0],pos[1]):
                    gvars.score+=1
                    gvars.fruit_count-=1
                    self.kill()
                    self. Sliced()
        
        
            def Sliced(self):
                pygame.mixer.Sound.play(cut_sound)
                radishcut1=RadishCut1(self.rect.x,self.rect.y,self.const)
                all_sprites.add(radishcut1)
                radishcut2=RadishCut2(self.rect.x,self.rect.y,self.const)
                all_sprites.add(radishcut2)
        
        class RadishCut1(pygame.sprite.Sprite):
            def __init__(self,x,y,velocity):
                
                pygame.sprite.Sprite.__init__(self)
                self.image=pygame.image.load(os.path.join(fruit_folder,"radishcut1.png")).convert_alpha()
                self.rect=self.image.get_rect()
                self.rect.x=x-150
                self.rect.y=y
                self.const=velocity
            def update(self):
                self.const+=0.4
                self.rect.y+=int(2*self.const)
                if self.rect.y>hight+200:
                    self.kill()
                    
        class RadishCut2(pygame.sprite.Sprite):
            def __init__(self,x,y,velocity):
                pygame.sprite.Sprite.__init__(self)
                self.image=pygame.image.load(os.path.join(fruit_folder,"radishcut2.png")).convert_alpha()
                self.rect=self.image.get_rect()
                self.rect.x=x-150
                self.rect.y=y
                self.const=velocity
            def update(self):
                self.const+=0.4
                self.rect.y+=int(2*self.const)
                if self.rect.y>hight+200:
                    self.kill()
        screen.fill((0,0,0))
        if musica_i:
            pygame.mixer.Sound.play(end_sound)
            musica_i=False
        background = pygame.image.load(os.path.join(background_folder,"startscreen.jpg")).convert()
        screen.fill([0,0,0])
        screen.blit(background, [0,0])
       
        draw_text('game', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
       
        pygame.display.update()
        mainClock.tick(60)
 
def options():
    musica_i=True
    running = True
    while running:
        screen.fill((0,0,0))
        background = pygame.image.load(os.path.join(background_folder,"startscreen.jpg")).convert()
        screen.fill([0,0,0])
        screen.blit(background, [0,0])
        if musica_i:
            pygame.mixer.Sound.play(end_sound)
            musica_i=False
            draw_text('options', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
       
        pygame.display.update()
        mainClock.tick(60)
 
main_menu()