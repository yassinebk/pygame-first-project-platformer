import pygame
from sys import exit

width = 800
height = 400
start_time = pygame.time.get_ticks()


def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - int(start_time/1000)
    score_surface = test_font.render('Score : '+str(current_time), False, (64, 64, 64)).convert_alpha()
    score_rect = score_surface.get_rect(center=(width / 2, 20))
    screen.blit(score_surface, score_rect)


pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = True

sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

# score_surface = test_font.render('Welcome', False, (64, 64, 64)).convert_alpha()
# score_rect = score_surface.get_rect(center=(400, 50))

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom=(width, height - ground_surface.get_height()))

player_surf = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom=(30, height - ground_surface.get_height()))

player_gravity = 0
player_stand =pygame.transform.scale2x(pygame.image.load('graphics/player/player_stand.png').convert_alpha())
player_stand_rect =player_stand.get_rect(center=(400,200))

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
                if event.key == pygame.K_SPACE:
                    player_gravity = -15
                    print('key down space')
            if event.type == pygame.KEYUP:
                print('key up')
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                snail_rect.left = width
                game_active = True
                start_time = pygame.time.get_ticks()

    # keys=pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]:
    #     print('jump')
    if game_active:
        screen.fill('BLACK')
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, height - ground_surface.get_height()))
        display_score()
        snail_rect.left -= 5
        if snail_rect.right < 0: snail_rect.left = width
        screen.blit(snail_surface, snail_rect)

        player_rect.bottom += player_gravity
        if player_gravity < 5 and player_rect.bottom != height - ground_surface.get_height():
            print('here')
            player_gravity += 1
        elif player_rect.bottom == height - ground_surface.get_height():
            player_gravity = 0
            player_rect.bottom = height - ground_surface.get_height()

        screen.blit(player_surf, player_rect)
    else:
        screen.fill((94,129,162))

    # Collision
    if snail_rect.colliderect(player_rect):
        game_active = False
        screen.blit(player_stand,player_stand_rect)

    pygame.display.update()
    clock.tick(60)
