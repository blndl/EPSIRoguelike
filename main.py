import pygame

class Event:
    def __init__(self):
        pass


class Render:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        self.screen.fill("white")
        pygame.draw.line(self.screen,"black",[1,50],[1000,50])
        pygame.draw.line(self.screen,"black",[1000,1],[1000,719])
        pygame.draw.line(self.screen,"black",[1000,200],[1279,200])
        pygame.draw.line(self.screen,"black",[1,450],[1279,450])
        pygame.draw.line(self.screen,"black",[1000,500],[1279,500])
        pygame.draw.line(self.screen,"black",[1000,550],[1279,550])

    

class Game:
    def __init__(self):
        self.render = Render()
        self.clock = pygame.time.Clock()
        self.running = True

game = Game()
while game.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            game.running = False

    
    pygame.display.flip()
    game.clock.tick(60)

pygame.quit()