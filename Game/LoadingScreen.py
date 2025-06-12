import pygame
import math
from Button import Button
from Levels import makeLevels
from Player import loadSkin

class Circle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = 255
        self.size = 20
    
    def update(self):
        self.color = max(self.color-4, 0)
        self.size = max(self.size-0, 0)
    
    def draw(self, WIN):
        c = int(self.color)
        pygame.draw.circle(WIN, (c, c, c), (self.x, self.y), self.size)


class LoadingAnimation:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.circles = []
    
    def update(self):
        x = self.x + math.cos(self.angle) * 75
        y = self.y + math.sin(self.angle) * 75
        self.circles.append(Circle(x, y))
        self.angle += 0.02
    
    def draw(self, WIN):
        for circle in self.circles:
            circle.draw(WIN)
            circle.update()
            if circle.color == 0:
                self.circles.remove(circle)

def LoadingScreen(thread, WIDTH, HEIGHT, WIN):
    loading = LoadingAnimation(WIDTH-110, HEIGHT-110)

    exitButton = Button((10, 10, 100, 50), "EXIT", (200, 0, 0), (100, 0, 0), 40)

    thread.start()
    
    makeLevels(WIDTH)
    loadSkin()

    while thread.is_alive():
        WIN.fill((0, 0, 0))
        
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                # press escape to close the game
                if event.key == pygame.K_ESCAPE:
                    return "quit"
        
        exitButton.draw(WIN)
        if exitButton.onClick():
            return "quit"

        loading.update()
        loading.draw(WIN)

        pygame.display.update()
    return "gameloop"