import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Effet d'éclaboussures")

FPS = 60
clock = pygame.time.Clock()

class Particle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = random.uniform(2, 4)
        self.angle = random.uniform(0, 2 * math.pi)
        self.gravity = 0.1
        self.y_velocity = random.uniform(-4, -2)

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed + self.y_velocity
        self.y_velocity += self.gravity
        self.speed *= 0.99

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))
class Water:
    def __init__(self, x, y, width, height, segments, tension=0.05, dampening=0.05):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.segments = segments
        self.spacing = self.width / (self.segments - 1)
        self.tension = tension
        self.dampening = dampening
        self.heights = [[0 for _ in range(segments)] for _ in range(2)]
        self.current_buffer = 0
    def update(self):
        for i in range(1, self.segments - 1):
            left_height = self.heights[self.current_buffer ^ 1][i - 1]
            right_height = self.heights[self.current_buffer ^ 1][i + 1]
            new_height = (left_height + right_height) / 2 - self.heights[self.current_buffer][i]

            new_height *= (1 - self.dampening)
            self.heights[self.current_buffer][i] = new_height

        self.current_buffer ^= 1

    def splash(self, index, amplitude):
        if 0 <= index < len(self.heights[self.current_buffer]):
            self.heights[self.current_buffer][index] = amplitude

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 255), (self.x, self.y, self.width, self.height))
        for i in range(1, len(self.heights[self.current_buffer])):
            x1 = self.x + self.spacing * (i - 1)
            y1 = self.y + self.heights[self.current_buffer ^ 1][i - 1]
            x2 = self.x + self.spacing * i
            y2 = self.y + self.heights[self.current_buffer ^ 1][i]
            pygame.draw.line(surface, (255, 255, 255), (x1, y1), (x2, y2), 2)




def create_splash_particles(x, y, n, particles):
    for _ in range(n):
        radius = random.uniform(1, 4)
        color = (0, 0, random.randint(200, 255))
        particle = Particle(x, y, radius, color)
        particles.append(particle)
player_rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, 50, 50)
water = Water(100, HEIGHT - 100, WIDTH - 200, 50, 40)
particles = []
splash = False

running = True
while running:
    WINDOW.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player_rect.x += 5
    if keys[pygame.K_UP]:
        player_rect.y -= 5
    if keys[pygame.K_DOWN]:
        player_rect.y += 5

    if player_rect.colliderect(water.x, water.y, water.width, water.height) and not splash:
        create_splash_particles(player_rect.x + player_rect.width // 2, player_rect.y + player_rect.height // 2, 50, particles)
        water_index = int((player_rect.x - water.x) // water.spacing)   
        water.splash(water_index, -20)
        splash = True
    elif not player_rect.colliderect(water.x, water.y, water.width, water.height):
        splash = False

    pygame.draw.rect(WINDOW, (255, 0, 0), player_rect)

    for particle in particles[:]:
        particle.move()
        particle.draw(WINDOW)
        if particle.radius < 0.1:
            particles.remove(particle)

    water.update()
    water.draw(WINDOW)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
