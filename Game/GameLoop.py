import pygame
from Player import handle_movement
from Player import Player
from Button import Button
from Camera import Camera
from Levels import getLevelPlatforms, getLevel

pygame.joystick.init()

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)  # Use the first joystick
    joystick.init()
else:
    print("No controller found")
    joystick = None

# load floor
floor_img = pygame.image.load("assets/floors/floor.png")

# returns the distance from one point to another
def getDistance(x, y, x1, y1):
    return ((x - x1)**2 + (y - y1)**2) ** 0.5

# draw everything in the gameloop that need to be drawn
def drawFrame(player, platforms, cam, WIDTH, HEIGHT, WIN, DeltaTime, CorrectSound, WrongSound, joystick, levelObj):

    levelObj.writeText(WIN, cam, WIDTH, HEIGHT)
    
    drawBG(cam, WIDTH, HEIGHT, WIN)

    for platform in platforms:
        if platform.isAlive:
            if getDistance(platform.rect.x, platform.rect.y, player.x, player.y) < WIDTH:
                platform.draw(cam, WIN, WIDTH, HEIGHT, DeltaTime, player, CorrectSound, WrongSound, joystick, platforms)
        platform.update()

    player.draw(cam, WIN, WIDTH, HEIGHT, DeltaTime)

# update everything that is player functions
def updatePlayer(player, platforms, cam, WIDTH, HEIGHT, DeltaTime, joystick):
    handle_movement(player, WIDTH, joystick, cam)
    player.addGravity(HEIGHT, cam, DeltaTime, WIDTH, floor_img)
    player.moveAnimation(DeltaTime)
    player.collidePlatform(platforms, HEIGHT, cam, floor_img)
    if player.play:
        player.move(DeltaTime)
    cam.follow_x = True if player.x > -100 + WIDTH/2 else False
    cam.follow_y = True if player.y > 50 else False

# draw the background and loop the floor
def drawBG(cam, WIDTH, HEIGHT, WIN):
    # floor
    x, y = cam.get(-100, HEIGHT/2 + 150, WIDTH, HEIGHT)
    pygame.draw.rect(WIN, (217, 211, 144), (x, y, floor_img.get_width(), 1000))
    WIN.blit(floor_img, (x, y))


def afterWinFunc(WIN, replayButton, mainMenuButton, nextLevelButton, currentLevel):
    replayButton.draw(WIN)
    mainMenuButton.draw(WIN)
    nextLevelButton.draw(WIN)
    if replayButton.onClick():
        return "loadingScreen", currentLevel
    if mainMenuButton.onClick():
        return "main-menu", None
    if nextLevelButton.onClick():
        return "loadingScreen", currentLevel+1
    

# main gameloop
def GameLoop(WIDTH, HEIGHT, WIN, FPS, CorrectSound, WrongSound, currentLevel):
    run = True
    clock = pygame.time.Clock()

    # the main player of the game initialize
    player = Player(WIDTH, HEIGHT)

    # sets all the platforms
    platforms = getLevelPlatforms()
    levelObj = getLevel()
    
    currentQuestionPlatform = None

    # set the camera
    cam = Camera()
    cam.x = player.x
    cam.y = player.y

    # set the quest which is the question show above the platform to be None at first
    quest = None

    # set the delta time -> delta time to run the game in the same speed anywhere
    DeltaTime = 1 / FPS

    # set the exit button
    exitButton = Button((WIDTH-110, 10, 100, 50), "BACK", (200, 0, 0), (100, 0, 0), 40)
    
    # after win buttons
    replayButton = Button((WIDTH/2-250-100, HEIGHT/2+100, 220, 100), "REPLAY STAGE", (0, 0, 255), (0, 0, 197), 40)
    mainMenuButton = Button((WIDTH/2-90, HEIGHT/2+100, 200, 100), "MAIN MENU", (0, 0, 255), (0, 0, 197), 40)
    nextLevelButton = Button((WIDTH/2+250-100, HEIGHT/2+100, 200, 100), "NEXT LEVEL", (0, 0 , 255), (0, 0, 197), 40)

    # variable to make the x button on a contoller work only once
    # without the otion to long press it
    longXpress = True
    
    while run:
        # fill the screen with the color blue
        WIN.fill((0, 200, 255))

        # pygame game events
        for event in pygame.event.get():
            # exit the screen when red x is pressed
            if event.type == pygame.QUIT:
                return "quit", None
            # keys events
            if event.type == pygame.KEYDOWN:
                # jump when space is pressed
                if event.key == pygame.K_SPACE and player.jump > 0 and player.play:
                    player.playerJump()
                # exit the game where the escape is pressed
                if event.key == pygame.K_ESCAPE:
                    return "main-menu", None
                
        if joystick:
            if joystick.get_button(0) and player.jump > 0 and player.play and not longXpress:
                player.playerJump()
                longXpress = True
            elif not joystick.get_button(0):
                longXpress = False

        # draws everything to the screen
        drawFrame(player, platforms, cam, WIDTH, HEIGHT, WIN, DeltaTime, CorrectSound, WrongSound, joystick, levelObj)
        # move the camera towards the player position
        cam.update(player.x, player.y, DeltaTime)
        # try and update the player, if it is colliding with a quest platform then its set the question as the quest
        updatePlayer(player, platforms, cam, WIDTH, HEIGHT, DeltaTime, joystick)

        # draw and make the exit button work
        exitButton.draw(WIN)
        if exitButton.onClick():
            return "main-menu", None

        # checks if the player has 0 life, and lose
        for x, heart in enumerate(player.life):
            if heart.life == 0:
                if x == 2:
                    return "lose-screen", None
                continue
            else:
                break
        
        if abs(platforms[-1].rect.y-platforms[-1].toTop) < 50:
            nextAction = afterWinFunc(WIN, replayButton, mainMenuButton, nextLevelButton, currentLevel)
            if nextAction:
                return nextAction

        # update the screen
        clock.tick(FPS)
        pygame.display.update()