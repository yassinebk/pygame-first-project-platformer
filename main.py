import pygame
from sys import exit
from random import randint, choice

width = 800
height = 400
start_time = pygame.time.get_ticks()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(200, height - ground_surface.get_height()))
        self.gravity = 0
        self.jump_sound=pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == height - ground_surface.get_height():
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        print(self.rect.bottom)
        if self.rect.bottom == height - ground_surface.get_height() and self.gravity != -20:
            self.rect.bottom = height - ground_surface.get_height()
            self.gravity = 0
            return
        self.gravity += 1
        self.rect.y += self.gravity

    def update(self):
        self.animation_state()
        self.player_input()
        self.apply_gravity()

    def animation_state(self):
        if self.rect.bottom < height - ground_surface.get_height():
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            self.fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            self.fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [self.fly_frame1, self.fly_frame2]
            y_pos = 110
        else:
            self.snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            self.frames = [self.snail_frame1, self.snail_frame2]
            y_pos = height - ground_surface.get_height()
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6

    def destroy(self):
        if self.rect.x <= -self.image.get_width():
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - int(start_time / 1000)
    score_surface = test_font.render('Score : ' + str(current_time), False, (64, 64, 64)).convert_alpha()
    score_rect = score_surface.get_rect(center=(width / 2, 20))
    screen.blit(score_surface, score_rect)
    return current_time


#
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    return True

# def obstacle_movement(obstacle_list):
#     if obstacle_list:
#         for obstacle_rect in obstacle_list:
#             obstacle_rect.x -= 5
#             if obstacle_rect.bottom == height - ground_surface.get_height():
#                 screen.blit(snail_surf, obstacle_rect)
#             else:
#                 screen.blit(fly_surf, obstacle_rect)
#         obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -obstacle.width]
#         return obstacle_list
#     else:
#         return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

#
# def player_animation():
#     global player_surf, player_index
#     if player_rect.bottom < height - ground_surface.get_height():
#         player_surf = player_jump
#     else:
#         player_index += 0.1
#         if player_index >= 2:
#             player_index = 0
#         player_surf = player_walk[int(player_index)]


pygame.init()

score = 0
game_active = False

bg_music=pygame.mixer.Sound('audio/music.wav')

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

obstacle_group = pygame.sprite.Group()
sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

# score_surface = test_font.render('Welcome', False, (64, 64, 64)).convert_alpha()
# score_rect = score_surface.get_rect(center=(400, 50))


player = pygame.sprite.GroupSingle()
player.add(Player())
# player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
# player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
# player_standby = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
# player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
# player_walk = [player_walk_1, player_walk_2]
# player_index = 0
# player_surf = player_walk[player_index]
# player_rect = player_standby.get_rect(midbottom=(30, height - ground_surface.get_height()))

player_gravity = 0

player_stand = pygame.transform.scale2x(pygame.image.load('graphics/player/player_stand.png').convert_alpha())
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press Space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 320))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1200)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


bg_music.play(loops=-1)
bg_music.set_volume(0.5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            # if event.type == pygame.MOUSEMOTION:
            #     if player_rect.collidepoint(event.pos):
            #         player_gravity = -20
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE and player_rect.bottom == height - ground_surface.get_height():
            #         player_gravity = -15
            # if event.type == pygame.KEYUP:
            print('key up')
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

    if game_active:
        screen.fill('BLACK')
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, height - ground_surface.get_height()))
        score = display_score()

        # if player_gravity < 5 and player_rect.bottom != height - ground_surface.get_height():
        #     player_gravity += 1

        # elif player_rect.bottom == height - ground_surface.get_height():
        #     player_gravity = 0
        #     player_rect.bottom = height - ground_surface.get_height()

        # player_animation()
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        game_active=collision_sprite()



    else:
        # player_rect.bottom = height - ground_surface.get_height()
        player_gravity = 0
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
