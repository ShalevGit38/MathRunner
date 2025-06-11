
from Platform import Platform
from random import randint
import pygame

maxLevel = 3
currentLevel = 1

font = pygame.font.Font(None, 100)

class Level:
    def __init__(self, WIDTH, number, hasFallings, hasQuestions, length, write):
        self.number = number
        self.hasFallings = hasFallings
        self.hasQuestions = hasQuestions
        self.length = length
        self.platforms = []
        self.write = write
        self.generateLevel(WIDTH)
    
    def generateLevel(self, WIDTH):
        firstPlatform = Platform((WIDTH-200, 600, 200, 40), False, False)
        self.platforms.append(firstPlatform)
        for i in range(self.length):
            self.addPlatform(i*600, WIDTH)
    
    def addPlatform(self, x, WIDTH):
        xPos = x+WIDTH+randint(100, 200)
        yPos = randint(300, 500)
        platform = Platform((xPos, yPos, 200, 40), self.hasFallings, self.hasQuestions)
        self.platforms.append(platform)
    
    def writeText(self, WIN, cam, WIDTH, HEIGHT):
        x, y = cam.get(1200, 200, WIDTH, HEIGHT)
        if x > -500:
            for i, text in enumerate(self.write):
                text_s = font.render(text, 1, (0, 0, 0))
                text_r = text_s.get_rect()
                # draw the outline of the text
                for j in [-1, 0, 1]:
                    for m in [-1, 0, 1]:
                        text_r.center = (x+(j*4), y+i*70+(m*4))
                        WIN.blit(text_s, text_r)
                # draw the inside of the text
                text_s = font.render(text, 1, (186, 192, 188))
                text_r = text_s.get_rect()
                text_r.center = (x, y+i*70)
                WIN.blit(text_s, text_r)


levels = []
def makeLevels(WIDTH):
    global levels
    levels = [
        # WIDTH, number, hasFallings, hasQuestions, platformsAmount, Text
        Level(WIDTH, 1, False, False, 10, ["LEVEL 1", "", "created by", "Shalev", "Tal", "Noam", "", "SPACE - jump  A - left  D - right"]),
        Level(WIDTH, 2, False, True, 12, ["LEVEL 2", "", "Now", "There are", "Questions!", "", "Press E", "to answer"]),
        Level(WIDTH, 3, True, True, 15, ["LEVEL 3", "", "Be carful", "the platforms", "are shaking"]),
        Level(WIDTH, 4, True, True, 17, ["LEVEL 4"]),
        Level(WIDTH, 5, True, True, 20, ["LEVEL 5"])
    ]

def getLevels():
    return levels

def getLevel():
    return levels[currentLevel-1]

def getLevelsAmount():
    return len(levels)

def getLevelPlatforms():
    return levels[currentLevel-1].platforms