# imports
import random
import pygame
from Player import Player
from Platform import Platform
import createProblem as eq
import threading
import time
import math

# initialize pygame
pygame.init()

# initialize the window
WIN = pygame.display.set_mode((0, 0))
WIDTH, HEIGHT = WIN.get_width(), WIN.get_height()
FPS = 144


# set the basic font
font = pygame.font.Font(None, 100)

#load music
file_path = 'assets/Pixelated Horizons.mp3'
pygame.mixer.music.load(file_path)
pygame.mixer.music.play(-1)

#button to turn off and on music
music_playing = True

# load images
floor = pygame.image.load("assets/floor.png")
bad_floor = pygame.image.load("assets/bad_floor.png")
name_image = pygame.image.load("assets/NINJA/name.png")
lose_image = pygame.image.load("assets/NINJA/lose.png")

# variable to the save the current screen / Mode
currentMode = "main-menu"

# called everytime a screen is changed to check what is the next screen
def changeMode():
    if currentMode == "gameloop":
        gameloop()
    elif currentMode == "loadingScreen":
        thread = threading.Thread(target=eq.createList, args=(100,))
        loadingScreen(thread)
    elif currentMode == "main-menu":
        MainMenu()
    elif currentMode == "lose-screen":
        LoseScreen()

# camera follow the player and set the position for everything else using the get method
class Camera:
    SPEED = 75

    def __init__(self):
        self.x = 0
        self.y = 0
        self.follow_y = True
        self.camShakeTime = 0

    # update the position of the camera to follow the x, y
    def update(self, x, y):
        self.x += (x - self.x) / self.SPEED
        if self.follow_y:
            self.y += (y - self.y) / (self.SPEED/10)
        if self.camShakeTime > 0 and False:
            self.x += random.randint(-5, 5)
            self.y += random.randint(-10, 10)
            self.camShakeTime -= 1

    # returns the position odf the object relative to the camera position
    def get(self, x, y):
        xPos = WIDTH/2 + (x - self.x) - 100
        yPos = HEIGHT/2 + (y - self.y)
        return xPos, yPos

# update everything that is player functions
def updatePlayer(player, platforms, cam, quest):
    quest = player.collidePlatform(platforms, WIDTH, HEIGHT, cam)
    player.addGravity(HEIGHT, cam)
    player.moveAnimation()
    if player.play:
        player.move()
    if player.y > 50:
        cam.follow_y = True
    else:
        cam.follow_y = False
    if quest:
        return quest

# handle the key press of the player movement
def handle_movement(player):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.move_right()
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.move_Left(WIDTH)
    else:
        player.currentSpeed = 0


# draw the background and loop the floor
def drawBG(cam, floors):
    # Background color behind floor
    _, y = cam.get(0, HEIGHT / 2 + 150)
    pygame.draw.rect(WIN, (217, 211, 144), (0, y, WIDTH, 600))

    # Draw the visible floor tiles
    for i in range(2):
        x, y = cam.get(floors[i], HEIGHT / 2 + 150)
        img = bad_floor if floors[i] > WIDTH else floor
        WIN.blit(img, (x, y))

    floor_width = floor.get_width()

    # Scroll logic - if camera moves right
    if cam.x - WIDTH/2+100 > floors[0] + floor_width:
        floors[0] = floors[1]
        floors[1] = floors[0] + floor_width

    # Scroll logic - if camera moves left
    elif cam.x + WIDTH/2+100 < floors[1]:
        floors[1] = floors[0]
        floors[0] = floors[1] - floor_width


# draw everything in the gameloop that need to be drawn
def drawEverything(player, platforms, cam, floors):
    drawBG(cam, floors)

    for platform in platforms:
        if getDistance(platform.rect.x, platform.rect.y, player.x, player.y) < WIDTH:
            platform.draw(cam, WIN)

    player.draw(cam, WIN)

# returns the distance from one point to another
def getDistance(x, y, x1, y1):
    return ((x - x1)**2 + (y - y1)**2) ** 0.5

# adds another platform to the x position at random y
def addPlatform(platforms, x):
    platforms.append(Platform((x+WIDTH+random.randint(150, 300), random.randint(300, 600), 200, 40)))

class Circle:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.color = 255
		self.size = 20
	
	def update(self):
		self.color = max(self.color-4, 0)
		self.size = max(self.size-0, 0)
	
	def draw(self):
		c = int(self.color)
		pygame.draw.circle(WIN, (c, c, c), (self.x, self.y), self.size)


class LoadingAnimation:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.angle = 0
		self.circles = []
	
	def update(self):
		x = self.x + math.cos(self.angle) * 100
		y = self.y + math.sin(self.angle) * 100
		self.circles.append(Circle(x, y))
		self.angle += 0.02
	
	def draw(self):
		for circle in self.circles:
			circle.draw()
			circle.update()
			if circle.color == 0:
				self.circles.remove(circle)

def loadingScreen(thread):
    global currentMode

    loading = LoadingAnimation(WIDTH/2, HEIGHT/2)

    exitButton = Button((10, 10, 100, 50), "EXIT", (200, 0, 0), (100, 0, 0), 40)

    thread.start()

    while thread.is_alive():
        WIN.fill((0, 0, 0))
        
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                # press escape to close the game
                if event.key == pygame.K_ESCAPE:
                    return
        
        exitButton.draw()
        if exitButton.onClick():
            return

        loading.update()
        loading.draw()

        pygame.display.update()
    currentMode = "gameloop"
    changeMode()

# main gameloop
def gameloop():
    global currentMode

    run = True
    clock = pygame.time.Clock()

    # the main player of the game initialize
    player = Player(HEIGHT)

    # sets all the platforms
    platforms = [Platform((WIDTH-200, 500, 200, 40))]
    for i in range(30):
        addPlatform(platforms, i*800)

    # set the camera
    cam = Camera()

    # set the floors x positions
    floors = [0, floor.get_width()]

    # set the quest which is the question show above the platform to be None at first
    quest = None

    # set the exit button
    exitButton = Button((WIDTH-110, 10, 100, 50), "EXIT", (200, 0, 0), (100, 0, 0), 40)

    while run:
        # fill the screen with the color blue
        WIN.fill((0, 200, 255))

        # pygame game events
        for event in pygame.event.get():
            # exit the screen when red x is pressed
            if event.type == pygame.QUIT:
                run = False
                return
            # keys events
            if event.type == pygame.KEYDOWN:
                # jump when space is pressed
                if event.key == pygame.K_SPACE and player.jump > 0 and player.play:
                    player.y -= 1
                    player.y_vel = -8
                    player.jump = 0
                    player.isInAir = True
                # exit the game where the escape is pressed
                if event.key == pygame.K_ESCAPE:
                    run = False
                    currentMode = "main-menu"
                    return

        # draws everything to the screen
        drawEverything(player, platforms, cam, floors)
        # moves the player
        handle_movement(player)
        # move the camera towards the player position
        cam.update(player.x, player.y)
        # try and update the player, and it is colliding with a quest platform then its set the q as the quest
        q = updatePlayer(player, platforms, cam, quest)
        if q:
            quest = q

        # draw the quest and update
        if quest:
            quest.draw(cam, WIN)
            answer = quest.update(player)
            if answer:
                quest = None

        # draw and make the exit button work
        exitButton.draw()
        if exitButton.onClick():
            currentMode = "main-menu"
            run = False

        # checks if the player has 0 life, and lose
        for x, heart in enumerate(player.life):
            if heart.life == 0:
                if x == 2:
                    currentMode = "lose-screen"
                    run = False
                continue
            else:
                break

        # update the screen
        clock.tick(FPS)
        pygame.display.update()
    # change game-mode if changed
    changeMode()


def LoseScreen():
    global currentMode

    run = True
    clock = pygame.time.Clock()

    # set all buttons
    mainMenuButton = Button((WIDTH/2-150, HEIGHT/2+400, 300, 100), "MENU", (0, 200, 0), (0, 100, 0), 100)
    exitButton = Button((10, 10, 100, 50), "EXIT", (200, 0, 0), (100, 0, 0), 40)

    while run:
        # fill the screen with a black color
        WIN.fill((0, 0, 0))

        # pygame game events
        for event in pygame.event.get():
            # exit the game when the red x is pressed
            if event.type == pygame.QUIT:
                run = False
                break
            # escape closing the game event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_RETURN:
                    currentMode = "main-menu"
                    run = False

        # draw buttons
        mainMenuButton.draw()
        exitButton.draw()

        # check if the buttons are pressed and react
        if mainMenuButton.onClick():
            currentMode = "main-menu"
            break
        if exitButton.onClick():
            return

        # show the loose text / image
        WIN.blit(lose_image, (WIDTH/4, 100))

        # update the screen
        pygame.display.update()
        clock.tick(FPS)
    # change the mode if changed
    changeMode()

# a class to make an easy window with a text
class Window:
    def __init__(self, text, x, y, size):
        self.text = text
        self.show = False
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, size)

    # draw the window if show is True
    def draw(self):
        if self.show:
            pygame.draw.rect(WIN, (255, 128, 0), (self.x, self.y, 500, 800), 0, 20)
            for y, txt in enumerate(self.text):
                text_s = self.font.render(txt, 1, (0, 0, 0))
                WIN.blit(text_s, (self.x+20, 200+y*40))

# class to make it easier to make a new button
class Button:
    def __init__(self, rect, text, color, toColor, size):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.toColor = toColor
        self.currentColor = self.color
        self.font = pygame.font.Font(None, size)
        self.clicked = False

    # draws the button
    def draw(self):
        pygame.draw.rect(WIN, self.currentColor, self.rect, 0, 10)
        pygame.draw.rect(WIN, (255, 255, 255), self.rect, 2, 10)
        self.drawText()

    # draws the buttons text
    def drawText(self):
        text_s = self.font.render(self.text, 1, (0, 0, 0))
        text_r = text_s.get_rect()
        text_r.center = (self.rect.x+self.rect.width/2, self.rect.y+self.rect.height/2)
        WIN.blit(text_s, text_r)

    # check if the button is being pressed and only once
    # and change the color at hover
    def onClick(self):
        mp = pygame.mouse.get_pressed()[0]
        mx, my = pygame.mouse.get_pos()
        if self.rect.x < mx < self.rect.x+self.rect.width and self.rect.y < my < self.rect.y+self.rect.height:
            self.currentColor = self.toColor
            if mp and not self.clicked:
                self.clicked = True
                return True
            if not mp:
                self.clicked = False
        else:
            self.currentColor = self.color
        return False

# the main menu screen
def MainMenu():
    global currentMode, music_playing
    run = True
    clock = pygame.time.Clock()

    #  pictures for the sound icon on/off
    path_music_on="assets/music logo/music_on"
    path_music_off="assets/music logo/music_off"

    # buttons on the main menu screen
    playButton = Button((WIDTH/2-150, HEIGHT/2+300, 300, 100), "PLAY", (0, 200, 0), (0, 100, 0), 100)
    exitButton = Button((10, 10, 100, 50), "EXIT", (200, 0, 0), (100, 0, 0), 40)
    helpButton = Button((10, 100, 50, 50), "?", (255, 128, 0), (155, 28, 0), 40)
    musicButton = Button((10, 200, 125, 50), "music", (0, 0, 255), (0, 0, 139), 60)


    # window that opens when I click on the help button
    helpWin = Window(
        ["a/arrow left -> move Left",
         "d/arrow right -> move right",
         "space -> jump",
         "enter -> choose answer"],
        150, 150, 50
    )

    # main loop in the main menu
    while run:
        WIN.fill((0, 0, 0))

        # pygame game events
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                # press escape to close the game
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_RETURN:
                    currentMode = "loadingScreen"
                    run = False
                    break

        # draw all the buttons
        playButton.draw()
        exitButton.draw()
        helpButton.draw()
        musicButton.draw()

        # check which button got clicked and their feature
        if playButton.onClick():
            currentMode = "loadingScreen"
            run = False
            break
        if exitButton.onClick():
            return
        if helpButton.onClick():
            helpWin.show = not helpWin.show
        if musicButton.onClick():
            music_playing = not music_playing
            if music_playing:
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.stop()


        # show the game name image
        WIN.blit(name_image, (WIDTH/4, -150))

        # draw the help menu
        helpWin.draw()

        # update the screen
        pygame.display.update()
        clock.tick(FPS)
    # change the screen in the end of the screen loop
    changeMode()

# start the game if I play this current file
if __name__ == "__main__":
    MainMenu()

# exit pygame if all windows closed
pygame.quit()
