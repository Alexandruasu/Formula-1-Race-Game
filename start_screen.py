import pygame
import sys
from config import window, width, height

# Încărcăm imaginea de fundal
background_image = pygame.image.load("imagini/fundal.png")
background_image = pygame.transform.scale(background_image, (width, height))

def draw_stylized_button(surface, x, y, width, height, text, font, color1, color2, border_color):
    """Funcție pentru a desena un buton lucios cu gradient."""
    # Desenăm gradientul
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

def start_screen():
    pygame.init()
    clock = pygame.time.Clock()

    # Fonturi
    title_font = pygame.font.Font(None, 74)
    button_font = pygame.font.Font(None, 48)

    while True:
        # Desenăm fundalul
        window.blit(background_image, (0, 0))

        # Textul titlului
        title_text = title_font.render("Simulare Circuit F1", True, (255, 255, 255))
        window.blit(title_text, (width // 2 - title_text.get_width() // 2, 50))

        # Desenăm butonul START
        button_x, button_y = width // 2 - 100, height // 2
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

        # Detectăm hover pentru buton
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
                    return  # Trecem la următorul ecran

        clock.tick(60)
