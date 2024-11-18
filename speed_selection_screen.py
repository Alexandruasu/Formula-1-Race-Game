import pygame
import sys
from config import window, width, height

def draw_gradient_background(surface, color1, color2):
    """Desenăm un gradient pe fundal."""
    for y in range(height):
        r = color1[0] + (color2[0] - color1[0]) * y // height
        g = color1[1] + (color2[1] - color1[1]) * y // height
        b = color1[2] + (color2[2] - color1[2]) * y // height
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))

def draw_stylized_button(surface, x, y, width, height, text, font, color1, color2, border_color):
    """Funcție pentru a desena un buton lucios cu gradient."""
    for i in range(height):
        r = color1[0] + (color2[0] - color1[0]) * i // height
        g = color1[1] + (color2[1] - color1[1]) * i // height
        b = color1[2] + (color2[2] - color1[2]) * i // height
        pygame.draw.line(surface, (r, g, b), (x, y + i), (x + width, y + i))

    # Desenăm conturul
    pygame.draw.rect(surface, border_color, (x, y, width, height), 5, border_radius=20)

    # Adăugăm textul
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surface, text_rect)

def clamp(value, min_value, max_value):
    """Limitează valoarea între min_value și max_value."""
    return max(min_value, min(value, max_value))

def speed_selection_screen(player_speed, bot_speed):
    pygame.init()
    clock = pygame.time.Clock()
    player_input_active = False
    bot_input_active = False
    player_input_text = str(player_speed)
    bot_input_text = str(bot_speed)

    # Fonturi
    title_font = pygame.font.Font(None, 74)
    button_font = pygame.font.Font(None, 48)
    input_font = pygame.font.Font(None, 36)

    MAX_SLIDER_WIDTH = 300  

    while True:
        draw_gradient_background(window, (200, 200, 200), (100, 100, 100))
        title_text = title_font.render("Setează vitezele", True, (0, 0, 0))
        window.blit(title_text, (width // 2 - title_text.get_width() // 2, 50))

        try:
            player_speed = clamp(int(player_input_text), 0, 100)
        except ValueError:
            player_speed = 0  

        try:
            bot_speed = clamp(int(bot_input_text), 0, 100)
        except ValueError:
            bot_speed = 0  

        player_slider_width = int((player_speed / 100) * MAX_SLIDER_WIDTH)
        bot_slider_width = int((bot_speed / 100) * MAX_SLIDER_WIDTH)

        player_slider = pygame.Rect(300, 200, player_slider_width, 20)
        bot_slider = pygame.Rect(300, 300, bot_slider_width, 20)
        pygame.draw.rect(window, (0, 255, 0), player_slider)
        pygame.draw.rect(window, (0, 255, 0), bot_slider)

        # Text pentru slidere
        player_text = input_font.render("Viteza Jucător:", True, (0, 0, 0))
        bot_text = input_font.render("Viteza Bot:", True, (0, 0, 0))
        window.blit(player_text, (100, 190))
        window.blit(bot_text, (100, 290))

        player_input_box = pygame.Rect(650, 190, 70, 40)
        bot_input_box = pygame.Rect(650, 290, 70, 40)

        pygame.draw.rect(window, (0, 255, 0) if player_input_active else (0, 0, 0), player_input_box, 2)
        pygame.draw.rect(window, (0, 255, 0) if bot_input_active else (0, 0, 0), bot_input_box, 2)

        # Textul din casetele de input
        player_input_surface = input_font.render(player_input_text, True, (0, 0, 0))
        bot_input_surface = input_font.render(bot_input_text, True, (0, 0, 0))
        window.blit(player_input_surface, (player_input_box.x + 5, player_input_box.y + 5))
        window.blit(bot_input_surface, (bot_input_box.x + 5, bot_input_box.y + 5))

        # Butonul START
        button_x, button_y = width // 2 - 100, height - 150
        button_width, button_height = 200, 80
        draw_stylized_button(
            window,
            button_x,
            button_y,
            button_width,
            button_height,
            "START",
            button_font,
            (50, 200, 50),  # Culoarea de sus (gradient)
            (0, 150, 0),  # Culoarea de jos (gradient)
            (0, 255, 0)  # Culoarea conturului
        )

        mouse_pos = pygame.mouse.get_pos()
        if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
            draw_stylized_button(
                window,
                button_x,
                button_y,
                button_width,
                button_height,
                "START",
                button_font,
                (100, 250, 100),  # Efect de hover
                (0, 200, 0),
                (255, 255, 0)  # Contur galben
            )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_x <= event.pos[0] <= button_x + button_width and button_y <= event.pos[1] <= button_y + button_height:
                    return player_speed, bot_speed  
                elif player_input_box.collidepoint(event.pos):
                    player_input_active = True
                    bot_input_active = False
                elif bot_input_box.collidepoint(event.pos):
                    bot_input_active = True
                    player_input_active = False
                else:
                    player_input_active = False
                    bot_input_active = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    player_input_active = False
                    bot_input_active = False
                if player_input_active:
                    if event.key == pygame.K_BACKSPACE:
                        player_input_text = player_input_text[:-1]
                    elif event.unicode.isdigit():
                        player_input_text += event.unicode
                        player_input_text = str(clamp(int(player_input_text), 0, 100))
                elif bot_input_active:
                    if event.key == pygame.K_BACKSPACE:
                        bot_input_text = bot_input_text[:-1]
                    elif event.unicode.isdigit():
                        bot_input_text += event.unicode
                        bot_input_text = str(clamp(int(bot_input_text), 0, 100))

        clock.tick(60)
