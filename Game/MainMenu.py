import pygame
from Button import Button
from Window import Window

name_image = pygame.image.load("assets/logos/name.png")
name_image = pygame.transform.scale(name_image, (name_image.get_width(), name_image.get_height()))

music_playing = True


# the main menu screen
def MainMenu(WIDTH, HEIGHT, WIN, FPS):
    global music_playing
    run = True
    clock = pygame.time.Clock()

    #  pictures for the sound icon on/off
    path_music_on = "assets/music logo/music_on"
    path_music_off = "assets/music logo/music_off"

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
                return "quit"
            if event.type == pygame.KEYDOWN:
                # press escape to close the game
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                if event.key == pygame.K_RETURN:
                    return "levelscreen"

        # draw all the buttons
        playButton.draw(WIN)
        exitButton.draw(WIN)
        helpButton.draw(WIN)
        musicButton.draw(WIN)

        # check which button got clicked and their feature
        if playButton.onClick():
            return "levelscreen"
        if exitButton.onClick():
            return "quit"
        if helpButton.onClick():
            helpWin.show = not helpWin.show
        if musicButton.onClick():
            music_playing = not music_playing
            if music_playing:
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.stop()


        # show the game name image
        WIN.blit(name_image, (WIDTH/2-name_image.get_width()/2, 0))

        # draw the help menu
        helpWin.draw(WIN)

        # update the screen
        pygame.display.update()
        clock.tick(FPS)