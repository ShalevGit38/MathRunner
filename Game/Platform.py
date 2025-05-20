import pygame
import random
from Player import removeHeart
import math
import createProblem as eq

pygame.init()

# load platforms and quest images
platform_image = pygame.image.load("assets/platform.png")
platform_image = pygame.transform.scale(platform_image, (200, 40))
quest_warning_image = pygame.image.load("assets/Ninja/!.png")
quest_warning_image = pygame.transform.scale(quest_warning_image, (quest_warning_image.get_width()/4, quest_warning_image.get_height()/4))

font = pygame.font.Font(None, 100)

# object of the platform
class Platform:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.moving = (random.randint(1, 5) <= 2)
        self.toTop = self.rect.y - 400
        self.moved = False

    # draw the platform using the camera
    def draw(self, cam, WIN):
        x, y = cam.get(self.rect.x, self.rect.y)
        #pygame.draw.rect(WIN, (0, 0, 0), (x, y, self.rect.width, self.rect.height))
        WIN.blit(platform_image, (x, y))
        if self.moving and not self.moved:
            WIN.blit(quest_warning_image, (x + quest_warning_image.get_width()/1.5, y - 100))

    # move the platform if it's a moving platform
    def move(self, player):
        if self.moving and not self.moved:
            player.play = False
            self.rect.y += (self.toTop - self.rect.y) / 50
            if abs(self.rect.y-self.toTop) < 50:
                self.moved = True
                quest_equation = random.choice(eq.equations)
                equationFixed = quest_equation.replace("÷", "/").replace("×", "*")
                quest = Quest(quest_equation, eval(equationFixed), self.rect.x+self.rect.width/2, self.rect.y-200)
                return quest

# the quest to draw the question and answers
class Quest:
    def __init__(self, quest, answer, x, y):
        self.quest = quest
        self.answer = int(answer) if answer == int(answer) else answer
        self.wrongAnswer = answer + (random.choice([-1, 1])*random.randint(1, 10))
        self.x = x
        self.y = y
        self.questMovement = 0
        self.correctIndex = random.randint(0, 1)
        self.choose = 0
        self.chooseX = 0

    # draw the answers and the quest
    def draw(self, cam, WIN):
        x, y = cam.get(self.x, self.y + math.sin(self.questMovement / 20) * 20)
        self.drawQuest(x, y, WIN)
        self.drawAnswer(x, y, WIN)
        self.drawChoose(x, y, WIN)

    # draw the choose one with a line
    def drawChoose(self, x, y, WIN):
        self.chooseX -= (self.chooseX - 400*self.choose) / 10
        pygame.draw.line(WIN, (255, 255, 0), ((x-200)+(self.chooseX)-100, y+50), ((x-200)+(self.chooseX)+100, y+50), 10)

    # draw the answer
    def drawQuest(self, x, y, WIN):
        self.questMovement += 1
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
    def update(self, player):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.choose = 0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.choose = 1
        if keys[pygame.K_SPACE] and self.questMovement > 50:
            if self.choose != self.correctIndex:
                removeHeart(player)
            player.play = True
            return True
        return False
