import pygame
import sys
font = None
# Créez une classe pour représenter une option de menu
class MenuOption:
    def __init__(self, text, pos, action):
        self.text = text
        self.pos = pos
        self.set_normal()
        self.action = action

    def draw(self, screen):
        screen.blit(self.text_surface, self.pos)

    def set_highlighted(self):
        self.text_surface = font.render(self.text, True, (255, 0, 0))

    def set_normal(self):
        self.text_surface = font.render(self.text, True, (255, 255, 255))

    def check_mouseover(self, mouse_pos):
        self.rect = self.text_surface.get_rect(topleft=self.pos)
        if self.rect.collidepoint(mouse_pos):
            self.set_highlighted()
            return True
        else:
            self.set_normal()
            return False

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.action()

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.Font(None, 64)
    clock = pygame.time.Clock()

    # Créer les options du menu
    menu_options = [
        MenuOption("Jouer", (100, 100), play_game),
        MenuOption("Réglages", (100, 200), settings),
        MenuOption("Crédits", (100, 300), credits),
        MenuOption("Quitter", (100, 400), quit_game),
    ]

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for option in menu_options:
                    option.check_click(mouse_pos)

        screen.fill((0, 0, 0))
        for option in menu_options:
            option.check_mouseover(mouse_pos)
            option.draw(screen)

        pygame.display.flip()
        clock.tick(60)

def play_game():
    print("Jouer au jeu")
    # Ajoutez votre boucle de jeu ici

def settings():
    print("Réglages")

def credits():
    print("Crédits")

def quit_game():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
