import pygame
import sys
from GameLogic.menu import Menu
from GameLogic.ingame import InGame
from GameLogic.Inventory import Inventory
from GameLogic.PauseMenu import PauseMenu
from GameLogic.calendar import Calendar



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("EPSI Rogue-Like")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"
        self.menu = Menu(self.screen)
        self.in_game= InGame(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.state == "menu":
                self.menu.handle_events(event)
                if self.menu.start_game:
                    self.state = "in_game"
            if self.state == "in_game":
                # self.game.handle_events(event)
                pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        if self.state == "menu":
            self.menu.draw()
        elif self.state == "in_game":
            self.in_game.draw()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
