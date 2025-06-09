
from Platform import Platform
from random import randint

maxLevel = 2
currentLevel = 1


class Level:
    def __init__(self, WIDTH, number, hasFallingPlatforms, length):
        self.number = number
        self.hasFallingPlatforms = hasFallingPlatforms
        self.length = length
        self.platforms = []
        self.generateLevel(WIDTH)
    
    def generateLevel(self, WIDTH):
        firstPlatform = Platform((WIDTH-200, 400, 200, 40))
        firstPlatform.isFallingPlatfrom = False
        firstPlatform.question = False
        platforms = [firstPlatform]
        for i in range(self.length):
            self.addPlatform(i*800, WIDTH)
    
    def addPlatform(self, x, WIDTH):
        xPos = x+WIDTH+randint(150, 250)
        yPos = randint(300, 500)
        platform = Platform((xPos, yPos, 200, 40))
        platform.isFallingPlatfrom = self.hasFallingPlatforms
        self.platforms.append(platform)


levels = []
def makeLevels(WIDTH):
    global levels
    levels = [
        Level(WIDTH, 1, False, 10),
        Level(WIDTH, 2, True, 12)
    ]

def getLevels():
    return levels