import pygame
import sys


pygame.init()

# Définir les couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = "#de8d4b"
fontt = "ressources/altertype-Regular.otf"
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")


bg_menu = pygame.image.load("ressources/bg_menu.png")






class Button:
    def __init__(self, x, y, w, h, text, font_size, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font_size = font_size
        self.action = action
        self.hovered = False

    def draw(self, surface):
        font = pygame.font.Font(fontt, self.font_size)
        text_color = RED if self.hovered else WHITE
        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                self.action()

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
def play():
    print("Jouer")

def settings():
    print("Réglages")

def credits():
    print("Crédits")

def quit_game():
    pygame.quit()
    sys.exit()

# Créer les boutons
buttons = [
    Button(WIDTH // 2 - 100, 320, 200, 50, "jouer", 33, play),
    Button(WIDTH // 2 - 100, 360, 200, 50, "reglages", 33, settings),
    Button(WIDTH // 2 - 100, 400, 200, 50, "credits", 33, credits),
    Button(WIDTH // 2 - 100, 440, 200, 50, "quitter", 31, quit_game),
]
title_font = pygame.font.Font(fontt, 160)
title_text = title_font.render("titre", True, WHITE)
title_rect = title_text.get_rect(center=(WIDTH // 2, 230))

version_font = pygame.font.Font(fontt, 15)
version_text = version_font.render("Ver 0.8", True, WHITE)
version_rect = version_text.get_rect(bottomright=(WIDTH - 10, HEIGHT - 10))

# Boucle principale
running = True
while running:
    # Afficher l'image de fond
    screen.blit(bg_menu, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for button in buttons:
            button.handle_event(event)

    # Afficher le titre et la version
    screen.blit(title_text, title_rect)
    screen.blit(version_text, version_rect)

    for button in buttons:
        button.update(mouse_pos)
        button.draw(screen)

    pygame.display.flip()

pygame.quit()