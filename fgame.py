#######################################################################################
# First Pygame Game.
# Honestly just playing around. Gonna use it for version management
# Author: Andrew Troyer
# Start Date: 6-8-21
# Start Location: Visalia CA, USA
#######################################################################################



import pygame
from pygame.locals import *

# Link, Start! ########################################################################

pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

HEIGHT = 450
WIDTH = 400
PLAYER_WIDTH = 30;
PLAYER_HEIGHT = 30;
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gaimu")

# Class Definitions #####################################################

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect()
        #Player Movement Variables
        self.pos = vec((15, 385))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        
    def move(self):
        self.acc = vec(0, 0.5)

        #Checks to see if any keys are pressed and gets which keys.
        pressed_keys = pygame.key.get_pressed()

        #Gives players left or right acceleration depending on left or right key press
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        #Fancy Shmancy movement
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        #Garbage Wrapping imo
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vel.y = -15

    def update(self):
        #Collision Detection
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if P1.vel.y > 0:
            if hits:
                self.pos.y= hits[0].rect.top + 1
                self.vel.y = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

# Object Obstantiation ##################################################

PT1 = Platform()
P1 = Player()

# Sprite Groups #########################################################

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(PT1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

# Game Loop ###########################################################################

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == QUIT or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_q)):
            pygame.quit()
            sys.exit()

    displaysurface.fill((0, 0, 0))
    P1.move()
    P1.update()

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)

# End Game Loop #######################################################################
