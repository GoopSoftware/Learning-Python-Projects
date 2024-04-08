import pygame
import sys


pygame.init()

# Handling the size of things
screen_width = 525
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
        self.rect.topleft = (grid_size, grid_size)
        self.move_timer = 0

    def move(self, dx, dy):
        if pygame.time.get_ticks() - self.move_timer > move_speed:
            new_x = self.rect.x + dx * grid_size
            new_y = self.rect.y + dy * grid_size

            temp_rect = self.rect.move(dx * grid_size, dy * grid_size)

            # Collision Detection
            obstacle_collision = False
            for obstacle in obstacles:
                if obstacle.rect.colliderect(temp_rect):
                    obstacle_collision = True
                    break

            if (border_size <= new_x <= screen_width - grid_size - border_size) and \
                    (border_size <= new_y <= screen_height - grid_size - border_size) and \
                    not obstacle_collision:
                self.rect.x = new_x
                self.rect.y = new_y
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


invalid_positions = [(0, 0, ), (grid_width - 1, grid_height - 1)]
obstacles = []

border_size = 35
border_width = 2
inner_grid_width = grid_width - 2 * border_width
inner_grid_height = grid_height - 2 * border_width

for x in range(border_width, border_width + inner_grid_width):
    for y in range(border_width, border_width + inner_grid_height):
        if x % 2 == 0 and y % 2 == 0:
            obstacles.append(Obstacle(x * grid_size, y * grid_size))

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

    pygame.draw.rect(screen, BLACK, (0, 0, screen_width, border_size))
    pygame.draw.rect(screen, BLACK, (0, 0, border_size, screen_height))
    pygame.draw.rect(screen, BLACK, (0, screen_height - border_size, screen_width, border_size))
    pygame.draw.rect(screen, BLACK, (screen_width - border_size, 0, border_size, screen_height))

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

    for obstacle in obstacles:
        screen.blit(obstacle.image, obstacle.rect)
    screen.blit(player.image, player.rect)

    # Collision detection
    collisions = pygame.sprite.spritecollide(player, obstacles, False)
    if collisions:
        print("Collision")


    if bomb:
        all_sprites.update()
        all_sprites.draw(screen)

    pygame.display.flip()

    pygame.time.Clock().tick(60)

    if bomb and bomb.exploded and pygame.time.get_ticks() - bomb.explosion_time > bomb_duration:
        bomb = None

pygame.quit()
sys.exit()