import pygame
from Player import handle_movement
from Player import Player
from Button import Button
from Camera import Camera
from Platform import Platform
from Platform import addPlatform

# load floors
floor = pygame.image.load("assets/floors/floor.png")
bad_floor = pygame.image.load("assets/floors/bad_floor.png")

# returns the distance from one point to another
def getDistance(x, y, x1, y1):
    return ((x - x1)**2 + (y - y1)**2) ** 0.5

# draw everything in the gameloop that need to be drawn
def drawEverything(player, platforms, cam, floors, WIDTH, HEIGHT, WIN):
    drawBG(cam, floors, WIDTH, HEIGHT, WIN)

    for platform in platforms:
        if getDistance(platform.rect.x, platform.rect.y, player.x, player.y) < WIDTH:
            platform.draw(cam, WIN, WIDTH, HEIGHT)

    player.draw(cam, WIN, WIDTH, HEIGHT)

# update everything that is player functions
def updatePlayer(player, platforms, cam, quest, WIDTH, HEIGHT):
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

# draw the background and loop the floor
def drawBG(cam, floors, WIDTH, HEIGHT, WIN):
    # Background color behind floor
    _, y = cam.get(0, HEIGHT / 2 + 150, WIDTH, HEIGHT)
    pygame.draw.rect(WIN, (217, 211, 144), (0, y, WIDTH, 600))

    # Draw the visible floor tiles
    for i in range(2):
        x, y = cam.get(floors[i], HEIGHT / 2 + 150, WIDTH, HEIGHT)
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


# main gameloop
def GameLoop(WIDTH, HEIGHT, WIN, FPS):
    run = True
    clock = pygame.time.Clock()

    # the main player of the game initialize
    player = Player(HEIGHT)

    # sets all the platforms
    platforms = [Platform((WIDTH-200, 500, 200, 40))]
    for i in range(30):
        addPlatform(platforms, i*800, WIDTH)

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
                return "quit"
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
                    return "main-menu"

        # draws everything to the screen
        drawEverything(player, platforms, cam, floors, WIDTH, HEIGHT, WIN)
        # moves the player
        handle_movement(player, WIDTH)
        # move the camera towards the player position
        cam.update(player.x, player.y)
        # try and update the player, and it is colliding with a quest platform then its set the q as the quest
        q = updatePlayer(player, platforms, cam, quest, WIDTH, HEIGHT)
        if q:
            quest = q

        # draw the quest and update
        if quest:
            quest.draw(cam, WIN, WIDTH, HEIGHT)
            answer = quest.update(player)
            if answer:
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

        # update the screen
        clock.tick(FPS)
        pygame.display.update()