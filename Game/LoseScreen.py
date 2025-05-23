import pygame
from Button import Button

lose_image = pygame.image.load("assets/logos/lose.png")

def LoseScreen(WIDTH, HEIGHT, WIN, FPS):
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
                return "quit"
            # escape closing the game event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                if event.key == pygame.K_RETURN:
                    return "main-menu"

        # draw buttons
        mainMenuButton.draw(WIN)
        exitButton.draw(WIN)

        # check if the buttons are pressed and react
        if mainMenuButton.onClick():
            return "main-menu"
        if exitButton.onClick():
            return "quit"

        # show the loose text / image
        WIN.blit(lose_image, (WIDTH/4, 100))

        # update the screen
        pygame.display.update()
        clock.tick(FPS)