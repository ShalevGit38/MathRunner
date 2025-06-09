from random import choice, randint
import pygame
from math import sin

cloudsImages = []

for i in range(6):
    img = pygame.image.load(f"assets/clouds/cloud{i + 1}.png")
    img = pygame.transform.scale(img, (img.get_width()/2, img.get_height()/2))
    cloudsImages.append(img)
    
    
# returns the distance from one point to another
def getDistance(x, y, x1, y1):
    return ((x - x1)**2 + (y - y1)**2) ** 0.5

# remove a cloud if the cloud is too much to the left
def removeClouds(clouds, cam, WIDTH):
    cloudsToRemove = []
    for cloud in clouds[:10]:
        if cloud.x < cam.x - WIDTH:
            cloudsToRemove.append(cloud)
    for cloud in cloudsToRemove:
        clouds.remove(cloud)
    
def spawnCloud(clouds, cam, WIDTH):
    if randint(1, 200) == 1:
        cloud = Cloud(cam.x+WIDTH, randint(-400, 500))
        clouds.append(cloud)
    
def drawClouds(clouds, WIN, WIDTH, HEIGHT, cam):
    for clouds in clouds:
        distance = getDistance(cam.x, cam.y, clouds.x, clouds.y)
        if distance < WIDTH:
            clouds.draw(WIN, WIDTH, HEIGHT, cam)
        clouds.update()

class Cloud:
    speed = 0.3
    upDownSpeed = 0.015
    upDownAmount = 15
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.upDownAngle = randint(0, 360)
        self.image = choice(cloudsImages)
    
    def draw(self, WIN, WIDTH, HEIGHT, cam):
        x, y = cam.get(self.x, self.y + sin(self.upDownAngle)*self.upDownAmount, WIDTH, HEIGHT)
        WIN.blit(self.image, (x, y))
        
    def update(self):
        self.x -= self.speed
        self.upDownAngle += self.upDownSpeed
        