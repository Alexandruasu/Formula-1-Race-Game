# game_loop.py

import pygame
import random
from config import *

def scale_speed(speed):
    return (speed / 100) * 7  # Viteza maximă va fi 7, minimă 0

def game_loop(player_speed, bot_speed):
    global car_x, car_y, car_image, bot_x, bot_y, bot_image, bot_direction  # Variabile globale pentru poziții și direcții

    bot_direction_cooldown = 0  # Cooldown pentru schimbarea direcției botului
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualizăm vitezele scalate
        scaled_player_speed = scale_speed(player_speed)
        scaled_bot_speed = scale_speed(bot_speed)

        # Controlul cu tastele W, A, S, D pentru jucător
        keys = pygame.key.get_pressed()
        new_x, new_y = car_x, car_y

        if keys[pygame.K_w]:  # W - în față
            new_y -= scaled_player_speed
            car_image = car_front
        elif keys[pygame.K_s]:  # S - în spate
            new_y += scaled_player_speed
            car_image = car_back
        elif keys[pygame.K_a]:  # A - stânga
            new_x -= scaled_player_speed
            car_image = car_left
        elif keys[pygame.K_d]:  # D - dreapta
            new_x += scaled_player_speed
            car_image = car_right

        new_x, new_y = constrain_to_track(new_x, new_y, car_image)

        if not check_collision(new_x, new_y, car_image, bot_x, bot_y, bot_image):
            car_x, car_y = new_x, new_y  

        # Mișcarea botului
        bot_new_x, bot_new_y = bot_x, bot_y

        if bot_direction == "up":
            bot_new_y -= scaled_bot_speed
            bot_image = car_front
        elif bot_direction == "down":
            bot_new_y += scaled_bot_speed
            bot_image = car_back
        elif bot_direction == "left":
            bot_new_x -= scaled_bot_speed
            bot_image = car_left
        elif bot_direction == "right":
            bot_new_x += scaled_bot_speed
            bot_image = car_right

        if (bot_new_x <= track_rect.left or
            bot_new_x + CAR_FRONT_BACK_WIDTH >= track_rect.right or
            bot_new_y <= track_rect.top or
            bot_new_y + CAR_FRONT_BACK_HEIGHT >= track_rect.bottom):
            if bot_direction_cooldown <= 0:
                valid_directions = []
                if bot_x > track_rect.left:
                    valid_directions.append("left")
                if bot_x + CAR_FRONT_BACK_WIDTH < track_rect.right:
                    valid_directions.append("right")
                if bot_y > track_rect.top:
                    valid_directions.append("up")
                if bot_y + CAR_FRONT_BACK_HEIGHT < track_rect.bottom:
                    valid_directions.append("down")

                if valid_directions:
                    bot_direction = random.choice(valid_directions)
                    bot_direction_cooldown = 30  

        bot_new_x, bot_new_y = constrain_to_track(bot_new_x, bot_new_y, bot_image)

        if not check_collision(bot_new_x, bot_new_y, bot_image, car_x, car_y, car_image):
            bot_x, bot_y = bot_new_x, bot_new_y 
        else:
            if bot_direction_cooldown <= 0:
                bot_direction = change_bot_direction()
                bot_direction_cooldown = 30  

        if bot_direction_cooldown > 0:
            bot_direction_cooldown -= 1

        window.fill(WHITE)
        pygame.draw.rect(window, BLACK, track_rect, 5) 

        window.blit(car_image, (car_x, car_y))  
        window.blit(bot_image, (bot_x, bot_y)) 

        pygame.display.flip()
        clock.tick(30)
