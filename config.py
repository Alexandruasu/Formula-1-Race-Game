# config.py

import pygame
import random

# Inițializare Pygame
pygame.init()

# Setări fereastră
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulare Circuit F1")

# Culori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Încărcarea imaginilor mașinii
car_front = pygame.image.load("imagini/sus.png")
car_back = pygame.image.load("imagini/jos.png")
car_left = pygame.image.load("imagini/stanga.png")
car_right = pygame.image.load("imagini/dreapta.png")

# Dimensiuni imagini mașină
CAR_FRONT_BACK_WIDTH = 54
CAR_FRONT_BACK_HEIGHT = 128
CAR_LEFT_RIGHT_WIDTH = 128
CAR_LEFT_RIGHT_HEIGHT = 53

# Configurare inițială
car_x, car_y = 150, 150
car_image = car_front  # Inițial orientat în față

bot_x, bot_y = random.randint(120, 680), random.randint(120, 480)
bot_image = car_front  # Inițial orientat în față
bot_direction = random.choice(["up", "down", "left", "right"])


# Circuit (rectangular)
track_rect = pygame.Rect(100, 100, 600, 400)

# Funcție de verificare a coliziunii
def check_collision(x1, y1, image1, x2, y2, image2):
    if image1 in [car_front, car_back]:
        rect1 = pygame.Rect(x1, y1, CAR_FRONT_BACK_WIDTH, CAR_FRONT_BACK_HEIGHT)
    else:  
        rect1 = pygame.Rect(x1, y1, CAR_LEFT_RIGHT_WIDTH, CAR_LEFT_RIGHT_HEIGHT)

    if image2 in [car_front, car_back]:
        rect2 = pygame.Rect(x2, y2, CAR_FRONT_BACK_WIDTH, CAR_FRONT_BACK_HEIGHT)
    else:  
        rect2 = pygame.Rect(x2, y2, CAR_LEFT_RIGHT_WIDTH, CAR_LEFT_RIGHT_HEIGHT)

    return rect1.colliderect(rect2)

# Funcție de menținere a mașinii în limitele circuitului
def constrain_to_track(x, y, image):
    if image in [car_front, car_back]:
        car_width, car_height = CAR_FRONT_BACK_WIDTH, CAR_FRONT_BACK_HEIGHT
    else:
        car_width, car_height = CAR_LEFT_RIGHT_WIDTH, CAR_LEFT_RIGHT_HEIGHT

    if x < track_rect.left:
        x = track_rect.left
    if x + car_width > track_rect.right:
        x = track_rect.right - car_width
    if y < track_rect.top:
        y = track_rect.top
    if y + car_height > track_rect.bottom:
        y = track_rect.bottom - car_height

    return x, y

# Funcție pentru schimbarea direcției botului
def change_bot_direction():
    return random.choice(["up", "down", "left", "right"])