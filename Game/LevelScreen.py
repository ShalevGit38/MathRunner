import pygame
from Button import Button

levels_image = pygame.image.load("assets/logos/levels.png")
levels_image = pygame.transform.scale(levels_image, (levels_image.get_width(), levels_image.get_height()))

def drawButtons(buttons, WIN, levelChoose):
    for button in buttons:
        button.draw(WIN)
        if button.text == str(levelChoose):
            pygame.draw.rect(WIN, (255, 255, 0), (button.rect), 5, 10)

def makeButtons(buttons, WIDTH, HEIGHT, levelsRow):
    for y in range(2):
        for x in range(5):
            size = 100
            buttonX = (WIDTH/2 - (size*5) + size/2) + x*size*2
            buttonY = (HEIGHT/2 - (size*2)/2) + y*size*2
            level = (x + y*5 + 1) + (levelsRow-1)*10
            buttons.append(Button((buttonX, buttonY, size, size), f"{level}", (0, 200, 0), (0, 100, 0), 75))

def LevelScreen(WIDTH, HEIGHT, WIN, FPS):
    run = True
    clock = pygame.time.Clock()
    
    levelChoose = 1
    levelsRow = 1
    
    buttons = []
    makeButtons(buttons, WIDTH, HEIGHT, levelsRow)
    
    exitButton = Button((WIDTH-110, 10, 100, 50), "BACK", (200, 0, 0), (100, 0, 0), 40)
    playButton = Button((WIDTH/2-150, HEIGHT/2+300, 300, 100), "PLAY", (0, 200, 0), (0, 100, 0), 100)
    
    while run:
        WIN.fill((0, 0, 0))
        
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                return "main-menu", None
            if event.type == pygame.KEYDOWN:
                # press escape to return to the main menu
                if event.key == pygame.K_ESCAPE:
                    return "main-menu", None
                if event.key == pygame.K_RIGHT:
                    levelsRow = min(levelsRow+1, 2)
                    makeButtons(buttons, WIDTH, HEIGHT, levelsRow)
                if event.key == pygame.K_LEFT:
                    levelsRow = max(levelsRow-1, 1)
                    makeButtons(buttons, WIDTH, HEIGHT, levelsRow)
                if event.key == pygame.K_RETURN:
                    return "loadingScreen", levelChoose
                
                ########*** make a button to PLAY the level, select a level before play
        
        # draw the buttons
        drawButtons(buttons, WIN, levelChoose)
        exitButton.draw(WIN)
        playButton.draw(WIN)
        
        # draw the levels logo
        WIN.blit(levels_image, (WIDTH/2-levels_image.get_width()/2, 0))
        
        for button in buttons:
            if button.onClick():
                levelChoose = int(button.text)
            
        if exitButton.onClick():
            return "main-menu", None
        if playButton.onClick():
            return "loadingScreen", levelChoose
        
        pygame.display.update()
        clock.tick(FPS)
    return "quit"