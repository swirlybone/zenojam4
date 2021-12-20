import pygame
from sprites import *
from config import *
import sys


class Game:
    def __int__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('Arial', 20)
        self.running = True

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates() #all sprites
        self.blocks = pygame.sprite.LayeredUpdates() #walls
        self.enemies = pygame.sprite.LayeredUpdates() #enemies
        self.attacks = pygame.sprite.LayeredUpdates() #attack

        self.player = Player(self, 1, 2)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
        

    def update(self):
        self.all_sprites.update()
        

    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while.self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):

    def intro_screen(self):

g = Game()
g.intro_screen()
g.new()
while g.running():
    g.main()
    g.game_over()
pygame.quit()
sys.exit()
        
