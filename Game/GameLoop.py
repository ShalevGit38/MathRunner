import pygame
from Player import handle_movement
from Player import Player
from Button import Button
from Camera import Camera
from Platform import Platform
from Platform import addPlatform
from Cloud import drawClouds, spawnCloud, removeClouds

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
def drawFrame(player, platforms, clouds, cam, WIDTH, HEIGHT, WIN, DeltaTime):
    drawClouds(clouds, WIN, WIDTH, HEIGHT, cam)
    
    drawBG(cam, WIDTH, HEIGHT, WIN)

    for platform in platforms:
        if getDistance(platform.rect.x, platform.rect.y, player.x, player.y) < WIDTH:
            if platform.isAlive:
                platform.draw(cam, WIN, WIDTH, HEIGHT)
            platform.update()

    player.draw(cam, WIN, WIDTH, HEIGHT, DeltaTime)

# update everything that is player functions
def updatePlayer(player, platforms, cam, quest, WIDTH, HEIGHT, DeltaTime, joystick):
    handle_movement(player, WIDTH, joystick, cam)
    player.addGravity(HEIGHT, cam, DeltaTime, WIDTH, floor_img)
    player.moveAnimation(DeltaTime)
    quest = player.collidePlatform(platforms, WIDTH, HEIGHT, cam, DeltaTime, floor_img)
    if player.play:
        player.move(DeltaTime)
    cam.follow_x = True if player.x > -100 + WIDTH/2 else False
    cam.follow_y = True if player.y > 50 else False
    if quest:
        return quest

# draw the background and loop the floor
def drawBG(cam, WIDTH, HEIGHT, WIN):
    # floor
    x, y = cam.get(-100, HEIGHT/2 + 150, WIDTH, HEIGHT)
    pygame.draw.rect(WIN, (217, 211, 144), (x, y, floor_img.get_width(), 1000))
    WIN.blit(floor_img, (x, y))


# main gameloop
def GameLoop(WIDTH, HEIGHT, WIN, FPS, CorrectSound, currentLevel):
    run = True
    clock = pygame.time.Clock()

    # the main player of the game initialize
    player = Player(WIDTH, HEIGHT)

    # sets all the platforms
    firstPlatform = Platform((WIDTH-200, 500, 200, 40))
    firstPlatform.isFallingPlatfrom = False
    firstPlatform.question = False
    platforms = [firstPlatform]
    for i in range(30):
        addPlatform(platforms, i*800, WIDTH)

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

    # variable to make the x button on a contoller work only once
    # without the otion to long press it
    longXpress = True
    
    print(currentLevel)
    
    clouds = []
    
    while run:
        # fill the screen with the color blue
        WIN.fill((0, 200, 255))

        # pygame game events
        for event in pygame.event.get():
            # exit the screen when red x is pressed
            if event.type == pygame.QUIT:
                return "quit"
            # keys events
            if event.type == pygame.KEYDOWN:
                # jump when space is pressed
                if event.key == pygame.K_SPACE and player.jump > 0 and player.play:
                    player.playerJump()
                # exit the game where the escape is pressed
                if event.key == pygame.K_ESCAPE:
                    return "main-menu"
                
        if joystick:
            if joystick.get_button(0) and player.jump > 0 and player.play and not longXpress:
                player.playerJump()
                longXpress = True
            elif not joystick.get_button(0):
                longXpress = False

        # draws everything to the screen
        drawFrame(player, platforms, clouds, cam, WIDTH, HEIGHT, WIN, DeltaTime)
        # move the camera towards the player position
        cam.update(player.x, player.y, DeltaTime)
        # try and update the player, if it is colliding with a quest platform then its set the question as the quest
        question = updatePlayer(player, platforms, cam, quest, WIDTH, HEIGHT, DeltaTime, joystick)
        if question:
            quest = question

        # draw the quest and update
        if quest:
            quest.draw(cam, WIN, WIDTH, HEIGHT, DeltaTime)
            answer = quest.update(player, CorrectSound, joystick)
            if answer:
                longXpress = True
                quest = None

        # draw and make the exit button work
        exitButton.draw(WIN)
        if exitButton.onClick():
            return "main-menu"

        # checks if the player has 0 life, and lose
        for x, heart in enumerate(player.life):
            if heart.life == 0:
                if x == 2:
                    return "lose-screen"
                continue
            else:
                break
        
        # spawn clouds on the screen
        spawnCloud(clouds, cam, WIDTH)
        # remove louds from the screen if too much to the left
        removeClouds(clouds, cam, WIDTH)

        # update the screen
        clock.tick(FPS)
        pygame.display.update()