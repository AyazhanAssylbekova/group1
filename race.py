#Imports
import pygame, sys
from pygame.locals import *
import random, time
 
#Initializing 
pygame.init()

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()
 
#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
count = 0
# bg_y = 0
#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

 
background = pygame.image.load("/Users/ayazhanassylbekova/Documents/group1/ani.png")
 
#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Create part-t classes
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("/Users/ayazhanassylbekova/Documents/group1/enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  
 
      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
       
        def __init__(self,value):
            super().__init__()
            self.image = pygame.image.load("/Users/ayazhanassylbekova/Documents/group1/coin.png")
            self.rect = self.image.get_rect()
            self.rect.center = (random.randint(40,SCREEN_WIDTH-40),0)
            self.value = value
            

        def move(self):
            # global SCORE
            self.rect.move_ip(0,SPEED)
            if (self.rect.top>600):
                # SCORE+=1
                # count+=1
                self.rect.top=0
                self.rect.center = (random.randint(40,SCREEN_WIDTH-40),0)
        # new pos if player get the point
        def reset(self):
            self.rect.top=0
            self.rect.center = (random.randint(40,SCREEN_WIDTH-40),0)
         
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("/Users/ayazhanassylbekova/Documents/group1/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
       #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, -5)
       #if pressed_keys[K_DOWN]:
            #self.rect.move_ip(0,5)
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                   
#Setting up Sprites        
P1 = Player()
E1 = Enemy()
C1 = Coin(random.randint(1,5))

 
#Creating Sprites Groups
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
enemies.add(E1)
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)
 
#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
 
#Game Loop
while True:
       
    #Cycles through all events occurring  

    for event in pygame.event.get():
        # after what point speed should increase
        if count%5==0 and count>0:
              SPEED +=0.5
              print(SPEED)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # pygame.display.update()

    # show(print) time in screen
    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    
    
 
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    
    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound("/Users/ayazhanassylbekova/Documents/group1/sound.wav").play()
          time.sleep(0.5)
                    
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
           
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit() 
        #increase points if player get it  
    if pygame.sprite.spritecollideany(P1, coins):
        count+=C1.value
        C1 = Coin(random.randint(1,5))
        
        # if player gets point it should start at the beginning
        for coin in coins:
            coin.reset()
    # show got points on screen 
    cnt=font_small.render(str(count), True, BLACK)
    DISPLAYSURF.blit(cnt,(10,50))


    pygame.display.update()
    FramePerSec.tick(FPS)