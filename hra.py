#Import veskerych veci
import pygame
from sys import exit
from random import randint, choice
import random

from pygame.sprite import AbstractGroup


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
            
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else: 
            self.player_index += 0.1
            if self.player_index > len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
            
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == "fly":
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1,snail_2]
            y_pos = 300
        
        self.animation_index = 0
        self.image = self.frames [self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900,1100),y_pos))

    def animation_state(self):
            self.animation_index += 0.1
            if self.animation_index > len(self.frames): self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]
            
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
        
#zobrazovani skore
def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 1000) #predelani na sekundy
    score_surface = test_font.render(f"Score: {current_time}", False, (64,64,64))
    score_rectangle = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rectangle)
    return current_time

#definovani pohybu objektu
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rectangle in obstacle_list:
            obstacle_rectangle.x -= 5
            
            if obstacle_rectangle.bottom == 300: screen.blit(snail_surface, obstacle_rectangle)
            else: screen.blit(fly_surface, obstacle_rectangle)
            
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

#definovani kolize
def collisions(player,obstacles):
    if obstacles:
        for obstacle_rectangle in obstacles:
            if player.colliderect(obstacle_rectangle): return False
    return True

#definovani kolize s jakymkoliv jinym spritem
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: 
        return True

#nastavovani animaci
def player_animation():
    global player_surface, player_index
    
    if player_rectangle.bottom < 300:
        player_surf = player_jump
    else:   
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surface = player_walk[int(player_index)]

#obecne nastaveni
pygame.init()
screen = pygame.display.set_mode((800,400)) #nastaveni velikosti okna
pygame.display.set_caption('Pixel Run BETA') #nastaveni nazvu
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf',50) #pridani fontu
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav') #pridani hudby
bg_music.play(loops = -1) #nastaveni na loop
bg_music.set_volume(0.2) #nastaveni hlasitosti


#Skupiny
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

#pridani nebe a zeme
sky_surface = pygame.image.load('graphics/Sky2.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

#Snek
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha() #alpha pomerne zbytecne ale je to potom vice plynule
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha() #alpha pomerne zbytecne ale je to potom vice plynule
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

#Moucha
fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha() #alpha pomerne zbytecne ale je to potom vice plynule
fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha() #alpha pomerne zbytecne ale je to potom vice plynule
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rectangle_list = []

player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha() #alpha pomerne zbytecne ale je to potom vice plynule
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha() #alpha pomerne zbytecne ale je to potom vice plynule
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha() #alpha pomerne zbytecne ale je to potom vice plynule

player_surface = player_walk[player_index]
player_rectangle = player_surface.get_rect(midbottom = (80,300))
player_gravity = 0

#Uvodni obrazovka
player_stand = pygame.image.load('graphics/Player/player_stand_red.png').convert_alpha() #alpha pomerne zbytecne ale je to potom vice plynule
player_stand = pygame.transform.rotozoom(player_stand, 0,2)
player_stand_rectangle = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Pixel Run', False, (111,196,169))
game_name_rectangle = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to play', False, (111,196,169))
game_message_rectangle = game_message.get_rect(center = (400, 330))

#Cas
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
                        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
                
        if game_active: 
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail','snail','snail',])))
  
                
    if game_active: 
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()

        #Vykreslovani hrace
        player.draw(screen)
        player.update()
        
        #Vykreslovani objektu
        obstacle_group.draw(screen)
        obstacle_group.update()

        #Kolize
        game_active = collision_sprite()
        
    #END obrazovka
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rectangle)
        obstacle_rectangle_list.clear()
        player_rectangle.midbottom = (80,300)
        game_over_rectangle = game_name.get_rect(center = (400,80))
        
        score_message = test_font.render(f'Your score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name, game_name_rectangle)
        

        
        if score == 0: screen.blit(game_message, game_message_rectangle)
        else: screen.blit(score_message, score_message_rect)
        
    #nastaveni obnovovani obrazovky (fps)  
    pygame.display.update()
    clock.tick(60)