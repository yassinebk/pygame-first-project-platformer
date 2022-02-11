import pygame
from sys import exit
from random import randint

width = 800
height = 400
start_time = pygame.time.get_ticks()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - int(start_time / 1000)
    score_surface = test_font.render('Score : ' + str(current_time), False, (64, 64, 64)).convert_alpha()
    score_rect = score_surface.get_rect(center=(width / 2, 20))
    screen.blit(score_surface, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom==height-ground_surface.get_height(): screen.blit(snail_surface, obstacle_rect)
            else: screen.blit(fly_surf, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -obstacle.width]
        return obstacle_list
    else:
        return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


pygame.init()

score = 0
game_active = False

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

obstacle_rect_list = []

sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

# score_surface = test_font.render('Welcome', False, (64, 64, 64)).convert_alpha()
# score_rect = score_surface.get_rect(center=(400, 50))

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
fly_surf = pygame.image.load('graphics/fly/fly1.png').convert_alpha()

player_surf = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom=(30, height - ground_surface.get_height()))

player_gravity = 0

player_stand = pygame.transform.scale2x(pygame.image.load('graphics/player/player_stand.png').convert_alpha())
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press Space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 320))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 900)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEMOTION:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom==height-ground_surface.get_height():
                    player_gravity = -15
            if event.type == pygame.KEYUP:
                print('key up')
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append( snail_surface.get_rect(bottomright=(randint(900, 1100), height - ground_surface.get_height())))
            else : obstacle_rect_list.append( fly_surf.get_rect(bottomright=(randint(900, 1100), height - ground_surface.get_height()-140)))

    # keys=pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]:
    #     print('jump')

    if game_active:
        screen.fill('BLACK')
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, height - ground_surface.get_height()))
        score = display_score()
        player_rect.bottom += player_gravity

        if player_gravity < 5 and player_rect.bottom != height - ground_surface.get_height():
            player_gravity += 1

        elif player_rect.bottom == height - ground_surface.get_height():
            player_gravity = 0
            player_rect.bottom = height - ground_surface.get_height()

        screen.blit(player_surf, player_rect)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        game_active=collisions(player_rect,obstacle_rect_list)


    else:
        player_rect.bottom=height-ground_surface.get_height()
        player_gravity=0
        obstacle_rect_list.clear()
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)
        score_message = test_font.render(f'Your score:{score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    # Collision

    pygame.display.update()
    clock.tick(60)
