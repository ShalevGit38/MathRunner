import pygame
import random
from Player import removeHeart
import math
import createProblem as eq

pygame.init()

# load platforms and quest images
platform_image = pygame.image.load(resource_path("assets/platforms/platform.png")
platform_image = pygame.transform.scale(platform_image, (200, 40))
quest_warning_image = pygame.image.load(resource_path("assets/platforms/questionSymbol.png")
quest_warning_image = pygame.transform.scale(quest_warning_image, (quest_warning_image.get_width()/4, quest_warning_image.get_height()/4))

font = pygame.font.Font(None, 100)

# adds another platform to the x position at random y
def addPlatform(platforms, x, WIDTH):
    platforms.append(Platform((x+WIDTH+random.randint(150, 250), random.randint(300, 500), 200, 40)))

# object of the platform
class Platform:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.question = (random.randint(1, 5) <= 2)
        self.hasQuestion = False
        self.correctAnswer = False
        self.quest = None
        self.toTop = self.rect.y - 400
        self.timeRemain = 0
        self.isAlive = True
        self.isFallingPlatfrom = True
        self.platformFall = False

    # draw the platform using the camera
    def draw(self, cam, WIN, WIDTH, HEIGHT, DeltaTime, player, CorrectSound, joystick):
        x, y = cam.get(self.rect.x, self.rect.y, WIDTH, HEIGHT)
        WIN.blit(platform_image, (x, y))
        if self.question and not self.hasQuestion:
            WIN.blit(quest_warning_image, (x + quest_warning_image.get_width()/1.5, y - 100))\
        
        # draw the quest and update
        if self.quest:
            self.quest.draw(cam, WIN, WIDTH, HEIGHT, DeltaTime)
            answer = self.quest.update(joystick)
            if answer == None:
                return
            if answer:
                self.correctAnswer = True
                CorrectSound.play()
                player.spawnPoint = (self.rect.x+self.rect.width/2-player.size/2, self.toTop-100)
            else:
                removeHeart(player)
            self.quest = False

    # move the platform if it's a moving platform
    def move(self, DeltaTime):
        if self.question and not self.hasQuestion:
            self.hasQuestion = True
            quest_equation = eq.equations[0]
            eq.equations.pop(0)
            equationFixed = quest_equation.replace("÷", "/").replace("×", "*")
            quest = Quest(quest_equation, eval(equationFixed), self.rect.x+self.rect.width/2, self.rect.y-200)
            return quest
    
    def update(self):
        if self.platformFall:
            self.timeRemain += 0.3
        if self.timeRemain >= 75 and not self.question and self.isFallingPlatfrom:
            self.rect.x = self.rect.x + math.cos(self.timeRemain)*3
            if self.timeRemain >= 125:
                self.isAlive = False
            if self.timeRemain >= 300:
                self.isAlive = True
                self.timeRemain = 0
                self.platformFall = False
        if self.correctAnswer:
            self.rect.y -= (self.rect.y - self.toTop) / 100

# the quest to draw the question and answers
class Quest:
    def __init__(self, quest, answer, x, y):
        self.quest = quest
        self.answer = int(answer) if answer == int(answer) else answer
        self.wrongAnswer = answer + (random.choice([-1, 1])*random.randint(2, 20))
        self.x = x
        self.y = y
        self.questMovement = 0
        self.correctIndex = random.randint(0, 1)
        self.choose = 0
        self.chooseX = 0

    # draw the answers and the quest
    def draw(self, cam, WIN, WIDTH, HEIGHT, DeltaTime):
        x, y = cam.get(self.x, self.y + math.sin(self.questMovement / 20) * 20, WIDTH, HEIGHT)
        self.drawQuest(x, y, WIN, DeltaTime)
        self.drawAnswer(x, y, WIN)
        self.drawChoose(x, y, WIN)

    # draw the choose one with a line
    def drawChoose(self, x, y, WIN):
        self.chooseX -= (self.chooseX - 400*self.choose) / 10
        pygame.draw.line(WIN, (255, 255, 0), ((x-200)+(self.chooseX)-100, y+50), ((x-200)+(self.chooseX)+100, y+50), 10)

    # draw the answer
    def drawQuest(self, x, y, WIN, DeltaTime):
        self.questMovement += 170*DeltaTime
        text_s = font.render(self.quest, 1, (0, 0, 0))
        text_r = text_s.get_rect()
        text_r.center = (x, y - 100)
        WIN.blit(text_s, text_r)

    # draw the quest
    def drawAnswer(self, x, y, WIN):
        text_s = font.render(f"{(self.wrongAnswer if not self.correctIndex else self.answer)}", 1, (0, 0, 0))
        text_r = text_s.get_rect()
        text_r.center = (x+200, y)
        WIN.blit(text_s, text_r)

        text_s = font.render(f"{(self.wrongAnswer if self.correctIndex else self.answer)}", 1, (0, 0, 0))
        text_r = text_s.get_rect()
        text_r.center = (x-200, y)
        WIN.blit(text_s, text_r)

    # update the choose one and set it by left and right arrow keys
    def update(self, joystick):
        keys = pygame.key.get_pressed()
        if joystick:
            joystickAmount = joystick.get_axis(0)
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) or (joystick and joystickAmount > 0.5):
            self.choose = 1
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) or (joystick and joystickAmount < -0.5):
            self.choose = 0
        if (keys[pygame.K_e] or (joystick and joystick.get_button(0))) and self.questMovement > 50:
            return not (self.choose != self.correctIndex)
