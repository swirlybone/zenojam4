import pygame
import math
import os
import random

pygame.init()

WIDTH, HEIGHT = (960, 640)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pest Exterminator")

WHITE = (250, 250, 250)
BLACK = (0, 0, 0)

FPS = 60
VEL = 4

PLAYER_WIDTH = 80
PLAYER_HEIGHT = 64
player_image_right = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "player.png")), (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_left = pygame.transform.flip(player_image_right, True, False)
player_blit_image = "right"
PLAYER_HEALTH = 20
player_died = False
player_vel_x = 0
player_vel_y = 0


class Bullet:

    BULLET_VEL = 6
    BULLET_DAMAGE = 5
    bullets = []

    def __init__(self, shooter, degrees, x, y, dx, dy):

        self.image = pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "bullet.png")), degrees)
        self.image_rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.shooter = shooter
        self.collided = False
        Bullet.bullets.append(self)

    def move(self):

        self.x += self.dx * self.BULLET_VEL
        self.y += self.dy * self.BULLET_VEL

    def collision_check(self, player):

        global PLAYER_HEALTH

        if player.x < self.x < player.x + player.width and player.y < self.y < player.y + player.height:

            self.collided = True
            PLAYER_HEALTH -= self.BULLET_DAMAGE

        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:

            self.collided = True

        if self.collided:

            self.shooter.bullets.remove(self)
            Bullet.bullets.remove(self)


class GhostWasp:

    WASP_IMAGE_GREEN = pygame.image.load(os.path.join("Assets", "ghost_green.png"))
    WASP_IMAGE_ORANGE = pygame.image.load(os.path.join("Assets", "ghost_orange.png"))
    WASP_IMAGE_PINK = pygame.image.load(os.path.join("Assets", "ghost_pink.png"))

    WASP_WIDTH = 39
    WASP_HEIGHT = 62
    WASP_VEL = 4
    WASP_BACK_VEL = 3
    BULLET_COOLDOWN = 60

    wasps = []

    def __init__(self, x, y):

        self.image_right = pygame.transform.scale(self.WASP_IMAGE_GREEN, (GhostWasp.WASP_WIDTH, GhostWasp.WASP_HEIGHT))
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image_to_blit = self.image_right
        self.image_rect = pygame.Rect(x, y, self.WASP_WIDTH, self.WASP_HEIGHT)
        GhostWasp.wasps.append(self)
        self.bullets = []
        self.cooldown = GhostWasp.BULLET_COOLDOWN

    def has_detected_player_check(self, player):

        return True if math.hypot(player.x - self.image_rect.x, player.y - self.image_rect.y) < 7 * 64 else False

    def move_towards_player(self, player):

        radians, distance, dx, dy = get_direction(self.image_rect.x + self.image_rect.width/2, self.image_rect.y + self.image_rect.height/2, player.x + player.width/2, player.y + player.height/2)

        if self.has_detected_player_check(player) and 3.5 * 64 < distance:

            self.image_to_blit = self.image_right if dx > 0 else self.image_left
            self.image_rect.x += dx * self.WASP_VEL
            self.image_rect.y += dy * self.WASP_VEL

        if 3.4 * 64 < distance < 3.6 * 64:

            # Move in a circle around the player.

            circumference = 2 * math.pi * 3.5 * 64
            

        elif 3 * 64 <= distance <= 3.6 * 64 and len(self.bullets) < 3 and not self.cooldown:

            self.shoot_bullet(radians, dx, dy)
            self.cooldown = GhostWasp.BULLET_COOLDOWN

        elif distance < 3 * 64:

            self.image_to_blit = self.image_right if dx > 0 else self.image_left
            self.image_rect.x -= dx * self.WASP_BACK_VEL
            self.image_rect.y -= dy * self.WASP_BACK_VEL

        if self.cooldown > 0:

            self.cooldown -= 1

    def shoot_bullet(self, radians, dx, dy):

        self.bullets.append(Bullet(self, math.degrees(radians), self.image_rect.x, self.image_rect.y, dx, dy))


# 1 and 2 refer to from and to positions respectively

def get_direction(x1, y1, x2, y2):

    radians = math.atan2(y2 - y1, x2 - x1)
    distance = int(math.hypot(x2-x1, y2-y1))

    dx = math.cos(radians)
    dy = math.sin(radians)

    return radians, distance, dx, dy


def handle_player_movement(keys_pressed):

    global player_blit_image, player_vel_x, player_vel_y

    if keys_pressed[pygame.K_a]:  # Left
        player_blit_image = "left"
        player_vel_x -= VEL
    if keys_pressed[pygame.K_d]:  # Right
        player_blit_image = "right"
        player_vel_x += VEL
    if keys_pressed[pygame.K_w]:  # Up
        player_vel_y -= VEL
    if keys_pressed[pygame.K_s]:  # Down
        player_vel_y += VEL


def draw_win(win, player, player_image_dir, wasps, bullets):
    win.fill(WHITE)
    win.blit(player_image_right if player_image_dir == "right" else player_image_left, (WIDTH/2 - player.width/2, HEIGHT/2 - player.height/2))

    for wasp in wasps:
        wasp.image_rect.x -= player_vel_x
        wasp.image_rect.y -= player_vel_y
        win.blit(wasp.image_to_blit, (wasp.image_rect.x, wasp.image_rect.y))

    for bullet in bullets:
        bullet.x -= player_vel_x
        bullet.y -= player_vel_y
        win.blit(bullet.image, (bullet.x, bullet.y))

    pygame.display.update()


def main():

    global player_vel_x, player_vel_y, player_died
    player = pygame.Rect(WIDTH/2 - PLAYER_WIDTH/2, HEIGHT/2 - PLAYER_HEIGHT/2, PLAYER_WIDTH, PLAYER_HEIGHT)
    world_data = [
        [1] * 15,
        *[[1] + [0] * 13 + [1]] * 13,
        [1] * 15
            ]
    #wasp1 = GhostWasp(64, 64)
    for x in range(5):
        GhostWasp(random.randint(0, WIDTH), random.randint(0, HEIGHT))

    clock = pygame.time.Clock()
    run = True

    while run:

        if player_died:

            WIN.fill(WHITE)

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        player_vel_x = 0
        player_vel_y = 0
        keys_pressed = pygame.key.get_pressed()
        handle_player_movement(keys_pressed)

        for wasp in GhostWasp.wasps:
            wasp.move_towards_player(player)

        for bullet in Bullet.bullets:
            bullet.move()
            bullet.collision_check(player)

        draw_win(WIN, player, player_blit_image, GhostWasp.wasps, Bullet.bullets)

        if PLAYER_HEALTH <= 0 :
            player_died = True
            #run = False

    pygame.quit()


if __name__ == "__main__":
    main()
