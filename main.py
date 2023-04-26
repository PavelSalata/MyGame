import pygame as py
import pygame.display, pygame.font
import random
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
from os import listdir
py.init()
FPS = py.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (250, 0, 0)
GREEN = (0, 255, 0)
DARK_CIAN = (0, 139, 139)

screen = width, height = 1024, 768  

font = py.font.SysFont('Verdana', 20)

main_surface = py.display.set_mode(screen)

IMAGES_PATH = 'goose'
player_images = [py.image.load(IMAGES_PATH + '/' + file).convert_alpha() for file in listdir(IMAGES_PATH)]
player = player_images[0]
player_rect = player.get_rect()                                                    
player_speed = 5

bg = py.transform.scale(py.image.load('background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

scores = 0


def create_enemy():
    enemy = py.image.load('enemy.png').convert_alpha()
    enemy_rect = py.Rect(width, random.randint(20, height-72), *enemy.get_size())
    enemy_speed = random.randint(3, 5)
    return [enemy, enemy_rect, enemy_speed]

CREATE_ENEMY = py.USEREVENT + 1
py.time.set_timer(CREATE_ENEMY, 1500)

enemies = []

def create_bonuses():
    bonus = py.image.load('bonus.png').convert_alpha()
    bonus_rect = py.Rect(random.randint(0, width-179), -bonus.get_height(), *bonus.get_size())
    bonus_speed = random.randint(1, 2)
    return [bonus, bonus_rect, bonus_speed]

CREATE_BONUSES = py.USEREVENT + 2
py.time.set_timer(CREATE_BONUSES, 2500)

bonuses = []

CHANGE_IMG = py.USEREVENT + 3
py.time.set_timer(CHANGE_IMG, 125)

image_index = 0

is_working = True   

while is_working: 
    FPS.tick(70)                             
    for event in py.event.get():
        if event.type == QUIT:
            # main_surface.blit(font.render(str(game_over_message), True, DARK_CIAN), (512, 364))
            is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        
        if event.type == CREATE_BONUSES:
            bonuses.append(create_bonuses())
        
        if event.type == CHANGE_IMG:
            image_index += 1
            if image_index == len(player_images):
                image_index = 0
            player = player_images[image_index]
    
    pressed_key = py.key.get_pressed()

    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < -bg.get_width():
        bgX = bg.get_width()
    
    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))

    main_surface.blit(player, (player_rect))

    main_surface.blit(font.render(str(scores), True, DARK_CIAN), (width - 30, 0))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < -300:
            enemies.pop(enemies.index(enemy))
        
        if player_rect.colliderect(enemy[1]):
            is_working = False
        
    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])
        
        if bonus[1].bottom > height:
            bonuses.pop(bonuses.index(bonus))
        
        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    if pressed_key[K_DOWN] and not player_rect.bottom >= height:
        player_rect = player_rect.move(0, player_speed)

    if pressed_key[K_UP] and not player_rect.top <= 0:
        player_rect = player_rect.move(0, -player_speed)
    
    if pressed_key[K_LEFT] and not player_rect.left <= 0:
        player_rect = player_rect.move(-player_speed, 0)
    
    if pressed_key[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed, 0)
    
    pygame.display.flip()

# Display "Game Over" message
game_over_font = py.font.SysFont('Verdana', 50)
game_over_text = game_over_font.render("Game Over", True, RED)
game_over_rect = game_over_text.get_rect(center=(width/2, height/2))

while True:
    main_surface.fill(BLACK)
    main_surface.blit(game_over_text, game_over_rect)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()