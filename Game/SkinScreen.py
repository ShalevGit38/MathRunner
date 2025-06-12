import pygame
from Button import Button
from Player import skins
from saveProgress import save, load

font = pygame.font.Font(None, 70)
little_font = pygame.font.Font(None, 40)

skins_image = pygame.image.load("assets/logos/skins.png")
skins_image = pygame.transform.scale(skins_image, (skins_image.get_width(), skins_image.get_height()))

needForSkins = [0, 10, 20, 40]

def drawQuestionAsnwered(WIN, questionsAnswered, WIDTH):
    text = f"Questions Answer- {questionsAnswered}"
    drawText(font, WIN, text, WIDTH/2, 815, (150, 150, 150))

def drawText(font, WIN, text, x, y, color):
    text_s = font.render(text, 1, color)
    text_r = text_s.get_rect()
    text_r.center = (x, y)
    WIN.blit(text_s, text_r)

def drawButtons(buttons, WIN, currentSkin, questionsAnswered):
    for x, button in enumerate(buttons):
        if not questionsAnswered >= needForSkins[x]:
            button.currentColor = (100, 100, 100)
            drawText(little_font, WIN, f"{needForSkins[x]}", button.rect.x+button.rect.width/2, button.rect.y+button.rect.height/2+150, (255, 255, 255))
        button.draw(WIN)
        if button.text == str(currentSkin):
            pygame.draw.rect(WIN, (255, 255, 0), (button.rect), 5, 10)
        skin_image = pygame.image.load(f"assets/skins/{button.text}/Idle/tile0.png")
        skin_image = pygame.transform.scale(skin_image, (skin_image.get_width()*2, skin_image.get_height()*2))
        WIN.blit(skin_image, (button.rect.x+button.rect.width/2-skin_image.get_width()/2, button.rect.y+button.rect.height/2-skin_image.get_height()/2+100))

def makeButtons(buttons, WIDTH, HEIGHT, levelsRow):
    for y in range(1):
        for x in range(5):
            skinNumber = (x + y*5 + 1) + (levelsRow-1)*10
            if skinNumber <= len(skins):
                size = 100
                buttonX  = (WIDTH/2 - size*4.5 + size/2) + x*size*2
                buttonY = (HEIGHT/2 - size*1 + size*1.5 + 200) + y*size*2
                buttons.append(Button((buttonX, buttonY, size*2, size), f"{skins[skinNumber-1]}", (0, 200, 0), (0, 100, 0), 75))


def SkinScreen(WIDTH, HEIGHT, WIN):
    run = True
    clock = pygame.time.Clock()
    
    exitButton = Button((WIDTH-110, 10, 100, 50), "BACK", (200, 0, 0), (100, 0, 0), 40)
    
    buttons = []
    makeButtons(buttons, WIDTH, HEIGHT, 1)
        
    currentSkin = load("skin")
    questionsAnswered = int(load("questionsAnswered"))
    
    while run:
        WIN.fill((0, 0, 0))
        
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                # press escape to return to the main menu
                if event.key == pygame.K_ESCAPE:
                    save("skin", currentSkin)
                    return "main-menu"
        
        
        exitButton.draw(WIN)
        drawButtons(buttons, WIN, currentSkin, questionsAnswered)
        
        if exitButton.onClick():
            save("skin", currentSkin)
            return "main-menu"
        for x, button in enumerate(buttons):
            if button.onClick():
                print(needForSkins[x], questionsAnswered)
                if questionsAnswered >= needForSkins[x]:
                    currentSkin = button.text
        
        # show the game skins image
        WIN.blit(skins_image, (WIDTH/2-skins_image.get_width()/2, 100))
        
        # show the amount of questions they answer
        drawQuestionAsnwered(WIN, questionsAnswered, WIDTH)
        
        pygame.display.update()
        clock.tick(120)
        
    return "quit"
        
    
    