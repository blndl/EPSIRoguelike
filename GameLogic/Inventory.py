class Inventory:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player

    def display_inventory(self):
        pass

    def draw_inventory(self):
        for item in self.player.bag:
            self.screen.blit(item.image, item.rect)
