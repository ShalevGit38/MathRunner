import pygame
from Button import Button

name_image = pygame.image.load("assets/logos/name.png")
name_image = pygame.transform.scale(name_image, (name_image.get_width(), name_image.get_height()))

music_playing = True


# the main menu screen
def MainMenu(WIDTH, HEIGHT, WIN, FPS):
    global music_playing
    run = True
    clock = pygame.time.Clock()

    # buttons on the main menu screen
    playButton = Button((WIDTH/2-150, HEIGHT/2+300, 300, 100), "PLAY", (0, 200, 0), (0, 100, 0), 100)
    exitButton = Button((10, 10, 100, 50), "EXIT", (200, 0, 0), (100, 0, 0), 40)
    musicButton = Button((WIDTH/2-75, HEIGHT/2+300-60, 150, 50), "music", (0, 255, 0), (0, 200, 0), 60)
    skinButton = Button((WIDTH/2-75, HEIGHT/2+400+10, 150, 50), "skins", (0, 200, 0), (0, 100, 0), 60)


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

        # check which button got clicked and their feature
        if playButton.onClick():
            return "levelscreen"
        if exitButton.onClick():
            return "quit"
        if skinButton.onClick():
            return "skinscreen"
        if musicButton.onClick():
            music_playing = not music_playing
            if music_playing:
                musicButton.color = (0, 255, 0)
                musicButton.toColor = (0, 200, 0)
                pygame.mixer.music.play(-1)
            else:
                musicButton.color = (255, 0, 0)
                musicButton.toColor = (200, 0, 0)
                pygame.mixer.music.stop()
        
        # draw all the buttons
        playButton.draw(WIN)
        exitButton.draw(WIN)
        musicButton.draw(WIN)
        skinButton.draw(WIN)


        # show the game name image
        WIN.blit(name_image, (WIDTH/2-name_image.get_width()/2, 0))

        # update the screen
        pygame.display.update()
        clock.tick(FPS)