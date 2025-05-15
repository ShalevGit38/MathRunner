import pygame
import time
import math

# load all the heart images
heart1 = pygame.image.load("assets/heart3.png")
heart1 = pygame.transform.scale(heart1, (heart1.get_width()*1.5, heart1.get_height()*1.5))
heart2 = pygame.image.load("assets/heart2.png")
heart2 = pygame.transform.scale(heart2, (heart2.get_width()*1.5, heart2.get_height()*1.5))
heart3 = pygame.image.load("assets/heart.png")
heart3 = pygame.transform.scale(heart3, (heart3.get_width()*1.5, heart3.get_height()*1.5))
hearts = [heart1, heart2, heart3]

# load animations
runAnimation = []
for i in range(12):
    image = pygame.image.load(f"assets/Ninja/NinjaRun/tile{i}.png")
    runAnimation.append(pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2)))

idleAnimation = []
for i in range(11):
    image = pygame.image.load(f"assets/Ninja/NinjaIdle/tile{i}.png")
    idleAnimation.append(pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2)))

image = pygame.image.load(f"assets/Ninja/fall.png")
fallAnimation = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))

image = pygame.image.load(f"assets/Ninja/jump.png")
jumpAnimation = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))

# heart class
class Heart:
    def __init__(self):
        self.life = 2
        self.countFrame = 0
        self.speed = 1

    # draw the heart by the current life that he has
    def draw(self, x, y, WIN):
        WIN.blit(hearts[self.life], (x, y + math.sin(self.countFrame/20)*10))
        self.countFrame += self.speed
        self.speed = max(self.speed-0.04, 1)

# player class
class Player:
    SPEED = 5
    GRAVITY = 0.0980665

    def __init__(self, HEIGHT):
        self.size = 50
        self.x = 0
        self.y = HEIGHT / 2 - self.size + 150
        self.color = (255, 0, 0)
        self.y_vel = 0
        self.jump = 1
        self.life = [Heart(), Heart(), Heart()]
        self.play = True
        self.currentFrame = 0
        self.lastTime = time.time()
        self.currentAnimation = 0
        self.direction = 0
        self.spawnPoint = (self.x, self.y)
        self.currentSpeed = 0
        self.isInAir = False


    # draw the player and animations
    def draw(self, cam, WIN):
        x, y = cam.get(self.x, self.y)
        draw_image = None

        if self.y_vel > 1:
            self.currentAnimation = 3
        elif self.y_vel < -1:
            self.currentAnimation = 4

        if self.currentAnimation == 0:
            draw_image = pygame.transform.flip(runAnimation[self.currentFrame%12], bool(self.direction), False)
        elif self.currentAnimation == 1:
            draw_image = pygame.transform.flip(runAnimation[self.currentFrame%12], bool(self.direction), False)
        elif self.currentAnimation == 2:
            draw_image = pygame.transform.flip(idleAnimation[self.currentFrame%11], bool(self.direction), False)
        elif self.currentAnimation == 3:
            draw_image = pygame.transform.flip(fallAnimation, bool(self.direction), False)
        elif self.currentAnimation == 4:
            draw_image = pygame.transform.flip(jumpAnimation, bool(self.direction), False)
        if draw_image:
            WIN.blit(draw_image, (x-10, y-10))

        self.currentAnimation = 2

        for x, heart in enumerate(self.life):
            heart.draw(0 + x*120, 0, WIN)
    
    # spawn the player to his last spawn point
    def spawn(self):
        self.x, self.y = self.spawnPoint

    # check where and if the player is colliding with the platforms
    def collidePlatform(self, platforms, WIDTH, HEIGHT, cam):
        selfRect = pygame.Rect(self.x, self.y, self.size, self.size)
        if self.y > HEIGHT-500 and self.x > WIDTH+500:
            self.spawn()
        for platform in platforms:
            if selfRect.colliderect(platform.rect):
                if self.x >= platform.rect.x+platform.rect.width-5:
                    self.jump = 1
                    self.x = platform.rect.x+platform.rect.width
                elif self.x+self.size <= platform.rect.x+5:
                    self.jump = 1
                    self.x = platform.rect.x-self.size
                elif self.y_vel >= 0:
                    if self.isInAir:
                        cam.camShakeTime = 25
                    self.isInAir = False
                    self.jump = 1
                    # set the player spawn point to the platfrom position when collide with it
                    self.spawnPoint = (platform.rect.x+platform.rect.width/2-self.size/2, platform.rect.y-100)
                    self.y_vel = 0
                    self.y = platform.rect.y - self.size
                    quest = platform.move(self)
                    if quest:
                        return quest
                elif self.y_vel < 0:
                    self.y_vel = 0
                    self.y = platform.rect.y+platform.rect.height
                return

    # make gravity effect the player
    def addGravity(self, HEIGHT, cam):
        self.y_vel += self.GRAVITY
        if self.y_vel > 0:
            self.y_vel += self.GRAVITY

        if self.y > HEIGHT/2-self.size+150:
            self.y_vel = 0
            self.y = HEIGHT/2-self.size+150
            self.jump = 1
            if self.isInAir:
                cam.camShakeTime = 25
            self.isInAir = False

        self.y += self.y_vel

    # move the player left
    def move_Left(self, WIDTH):
        if self.x > -WIDTH/2 and self.play:
            self.currentSpeed = -self.SPEED
        self.currentAnimation = 1
        self.direction = 1

    # move the player right
    def move_right(self):
        if self.play:
            self.currentSpeed = self.SPEED
        self.currentAnimation = 0
        self.direction = 0
    
    def move(self):
        self.x += self.currentSpeed
        if abs(self.y_vel) > self.GRAVITY*2:
            self.isInAir = True

    # skip by the animations to make the run and idle smooth
    def moveAnimation(self):
        if abs(time.time()-self.lastTime) > 0.04:
            self.currentFrame += 1
            self.lastTime = time.time()

# remove heart when getting damage
def removeHeart(player):
    for heart in reversed(player.life):
        if heart.life > 0:
            heart.life -= 1
            break
    for heart in player.life:
        heart.speed = 7