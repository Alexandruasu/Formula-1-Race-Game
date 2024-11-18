# main.py
import pygame
import sys
from start_screen import start_screen
from speed_selection_screen import speed_selection_screen
from game_loop import game_loop

# Inițializăm vitezele în main.py
player_speed = 1
bot_speed = 30

# Rularea jocului
start_screen()
player_speed, bot_speed = speed_selection_screen(player_speed, bot_speed)
game_loop(player_speed, bot_speed)

pygame.quit()
sys.exit()
