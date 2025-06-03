import pygame
from Button import Button



def drawButtons(buttons, WIN):
    for button in buttons:
        button.draw(WIN)

def LevelScreen(WIDTH, HEIGHT, WIN, FPS):
    run = True
    clock = pygame.time.Clock()
    
    buttons = []
    for y in range(2):
        for x in range(5):
            buttons.append(Button(((WIDTH/2-5*100) + x*200, (HEIGHT/2-2*100) + y*200, 100, 100), f"{x + y*5 + 1}", (0, 200, 0), (0, 100, 0), 75))
    
    exitButton = Button((WIDTH-110, 10, 100, 50), "BACK", (200, 0, 0), (100, 0, 0), 40)
    
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
                #if event.key == pygame.K_RETURN:
                    #return "loadingScreen", None
                
                ########*** make a button to PLAY the level, select a level before play
        
        # draw the buttons
        drawButtons(buttons, WIN)
        exitButton.draw(WIN)
        
        for button in buttons:
            if button.onClick():
                return "loadingScreen", button.text
            
        if exitButton.onClick():
            return "main-menu", None
        
        pygame.display.update()
        clock.tick(FPS)
    return "quit"