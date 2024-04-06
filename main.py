import pygame
import sys


pygame.init()

# Handling the size of things
screen_width = 700
screen_height = 525
grid_size = 35
obstacle_size = 35
grid_width = screen_width // grid_size
grid_height = screen_height // grid_size

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


# Handles the speed of things and the game tick durations
move_speed = 150
bomb_explode_delay = 2000
bomb_duration = 1000

# Game Screen
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


class Bomb(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()
        self.image = pygame.Surface((grid_size, grid_size))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # bomb position
        self.rect.centerx = player_rect.centerx
        self.rect.centery = player_rect.centery
        # Bomb explode timer and explosion time
        self.explode_timer = pygame.time.get_ticks() + bomb_explode_delay
        self.exploded = False
        self.explosion_time = None

    def update(self):
        if not self.exploded:
            if pygame.time.get_ticks() >= self.explode_timer:
                self.explode()
        elif pygame.time.get_ticks() - self.explosion_time > bomb_duration:
            self.kill()
    def explode(self):
        self.exploded = True
        self.explosion_time = pygame.time.get_ticks()
        print("Bomb exploded")

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((obstacle_size, obstacle_size))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


obstacles = []
for x in range(grid_size, screen_width - grid_size, grid_size):
    for y in range(grid_size, screen_height - grid_size, grid_size):
        if (x, y) != (grid_width * 2, grid_height * 2):
            obstacles.append(Obstacle(x, y))
player = Player()
bomb = None
all_sprites = pygame.sprite.Group()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    # Draw grid for debugging
    #for x in range(0, screen_width, grid_size):
        #pygame.draw.line(screen, BLACK, (x, 0), (x, screen_height))
    #for y in range(0, screen_height, grid_size):
        #pygame.draw.line(screen, BLACK, (0, y), (screen_width, y))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.move(-1, 0)
    if keys[pygame.K_d]:
        player.move(1, 0)
    if keys[pygame.K_w]:
        player.move(0, -1)
    if keys[pygame.K_s]:
        player.move(0, 1)
    if keys[pygame.K_SPACE] and not bomb:
        bomb = Bomb(player.rect)
        all_sprites.add(bomb)


    pygame.draw.rect(screen, BLACK, (0, 0, screen_width, screen_height), 1)
    screen.blit(player.image, player.rect)
    if bomb:
        all_sprites.update()
        all_sprites.draw(screen)
        #screen.blit(bomb.image, bomb.rect)

    collisions = pygame.sprite.spritecollide(player, obstacles, False)
    if collisions:
        print("Collision")



    obstacle = Obstacle(grid_size, grid_size)
    obstacles = pygame.sprite.Group(obstacle)
    for obstacle in obstacles:
        screen.blit(obstacle.image, obstacle.rect)
    screen.blit(obstacle.image, obstacle.rect)
    pygame.display.flip()

    pygame.time.Clock().tick(60)

    if bomb and bomb.exploded and pygame.time.get_ticks() - bomb.explosion_time > bomb_duration:
        bomb = None

pygame.quit()
sys.exit()