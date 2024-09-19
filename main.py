import pygame
import sys
import os
from GameLogic.menu import Menu
from GameLogic.ingame import InGame
from GameLogic.Inventory import Inventory
from GameLogic.PauseMenu import PauseMenu
from GameLogic.player import Player
from GameLogic.shop import Shop
from generator import Month
from GameLogic.tuto import Tutorial  # Importez le tutoriel


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("EPSImester")
        self.clock = pygame.time.Clock()
        self.running = True
        self.month = Month()
        self.seed = self.month.return_month()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        self.state = "menu"  # Commencez par le menu
        self.font = "pixeboy.ttf"

        self.player = Player("Gin")

        self.menu = Menu(self.screen)
        self.tutorial = Tutorial(self.screen)  # Instance du tutoriel
        self.in_game = InGame(self.screen, self.player, self.seed, self)
        self.pause_menu = PauseMenu(self.screen, self)
        self.inventory = Inventory(self, self.screen, self.player)
        self.shop = Shop(self.screen, self.player, self.in_game, self)

        pygame.mixer.music.load("Sounds/main_music.mp3")
        pygame.mixer.music.play(loops=-1)  # Play music in a loop indefinitely

        pygame.mixer.set_num_channels(2)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.state == "menu":
                self.menu.handle_events(event)
                if self.menu.start_game:
                    self.state = "tutorial"  # Passer au tutoriel quand le jeu commence

            elif self.state == "tutorial":
                self.tutorial.handle_events(event)
                if not self.tutorial.running:
                    self.state = "in_game"  # Passer au jeu après le tutoriel

            elif self.state == "in_game":
                self.in_game.handle_events(event)
            elif self.state == "pause_menu":
                self.pause_menu.handle_events(event)
            elif self.state == "inventory":
                self.inventory.handle_events(event)
            elif self.state == "shop":
                self.shop.handle_events(event)

    def draw(self):
        if self.state == "menu":
            print("Drawing menu")  # Debugging statement
            self.menu.draw()
        elif self.state == "tutorial":
            print("Drawing tutorial")  # Debugging statement
            self.tutorial.draw()
        elif self.state == "in_game":
            print("Drawing in-game")  # Debugging statement
            self.in_game.draw()
        elif self.state == "inventory":
            print("Drawing inventory")  # Debugging statement
            self.inventory.draw_inventory()
        elif self.state == "pause_menu":
            print("Drawing pause menu")  # Debugging statement
            self.pause_menu.draw()
        elif self.state == "shop":
            print("Drawing shop")  # Debugging statement
            self.shop.draw()

        # Update the display
        pygame.display.flip()

    def run(self):
        pygame.mixer.init()
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)

            if self.state == "shop" and not self.shop.sound_played:
                self.shop.play_shop_sound()
                self.shop.sound_played = True
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
