import pygame
import sys


pygame.init()

screen_width = 700
screen_height = 525
grid_size = 35
grid_width = screen_width // grid_size
grid_height = screen_height // grid_size

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

move_speed = 150

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My game")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((grid_size, grid_size))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.move_timer = 0

    def move(self, dx, dy):
        if pygame.time.get_ticks() - self.move_timer > move_speed:
            self.rect.x += dx * grid_size
            self.rect.y += dy * grid_size

            # Resctricts movement to the bounds of the window
            self.rect.x = max(0, min(self.rect.x, screen_width - grid_size))
            self.rect.y = max(0, min(self.rect.y, screen_height - grid_size))
            self.move_timer = pygame.time.get_ticks()

player = Player()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    # Draw grid for debugging
    for x in range(0, screen_width, grid_size):
        pygame.draw.line(screen, BLACK, (x, 0), (x, screen_height))
    for y in range(0, screen_height, grid_size):
        pygame.draw.line(screen, BLACK, (0, y), (screen_width, y))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.move(-1, 0)
    if keys[pygame.K_d]:
        player.move(1, 0)
    if keys[pygame.K_w]:
        player.move(0, -1)
    if keys[pygame.K_s]:
        player.move(0, 1)




    pygame.draw.rect(screen, BLACK, (0, 0, screen_width, screen_height), 1)
    screen.blit(player.image, player.rect)

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()