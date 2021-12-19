import pygame
import math
import os

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
player_vel_x = 0
player_vel_y = 0


class GhostWasp:

    WASP_IMAGE_GREEN = pygame.image.load(os.path.join("Assets", "ghost_green.png"))
    WASP_IMAGE_ORANGE = pygame.image.load(os.path.join("Assets", "ghost_orange.png"))
    WASP_IMAGE_PINK = pygame.image.load(os.path.join("Assets", "ghost_pink.png"))

    WASP_WIDTH = 39
    WASP_HEIGHT = 62
    WASP_VEL = 4
    WASP_BACK_VEL = 3

    wasps = []

    def __init__(self, x, y):

        self.image_right = pygame.transform.scale(self.WASP_IMAGE_GREEN, (GhostWasp.WASP_WIDTH, GhostWasp.WASP_HEIGHT))
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image_to_blit = self.image_right
        self.image_rect = pygame.Rect(x, y, self.WASP_WIDTH, self.WASP_HEIGHT)
        GhostWasp.wasps.append(self)

    def has_detected_player_check(self, player):

        return True if math.hypot(player.x - self.image_rect.x, player.y - self.image_rect.y) < 7 * 64 else False

    def move_towards_player(self, player):

        distance, dx, dy = get_direction(self.image_rect.x, self.image_rect.y, player.x, player.y)

        if self.has_detected_player_check(player) and 3.5 * 64 < distance:

            self.image_to_blit = self.image_right if dx > 0 else self.image_left
            self.image_rect.x += dx * self.WASP_VEL
            self.image_rect.y += dy * self.WASP_VEL

        elif distance < 3 * 64:

            self.image_to_blit = self.image_right if dx > 0 else self.image_left
            self.image_rect.x -= dx * self.WASP_BACK_VEL
            self.image_rect.y -= dy * self.WASP_BACK_VEL


# 1 and 2 refer to from and to positions respectively

def get_direction(x1, y1, x2, y2):

    radians = math.atan2(y2 - y1, x2 - x1)
    distance = int(math.hypot(x2-x1, y2-y1))

    dx = math.cos(radians)
    dy = math.sin(radians)

    return distance, dx, dy


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


def draw_win(win, player, player_image_dir, wasps):
    win.fill(WHITE)
    win.blit(player_image_right if player_image_dir == "right" else player_image_left, (WIDTH/2 - player.width/2, HEIGHT/2 - player.height/2))

    for wasp in wasps:
        #pygame.draw.rect(win, BLACK, wasp.image_rect)
        wasp.image_rect.x -= player_vel_x
        wasp.image_rect.y -= player_vel_y
        win.blit(wasp.image_to_blit, (wasp.image_rect.x, wasp.image_rect.y))

    pygame.display.update()


def main():

    global player_vel_x, player_vel_y
    player = pygame.Rect(WIDTH/2 - PLAYER_WIDTH/2, HEIGHT/2 - PLAYER_HEIGHT/2, PLAYER_WIDTH, PLAYER_HEIGHT)
    world_data = [
        [1] * 15,
        *[[1] + [0] * 13 + [1]] * 13,
        [1] * 15
            ]
    wasp1 = GhostWasp(64, 64)

    clock = pygame.time.Clock()
    run = True

    while run:
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

        draw_win(WIN, player, player_blit_image, GhostWasp.wasps)

    pygame.quit()


if __name__ == "__main__":
    main()
