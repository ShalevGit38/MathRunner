import pygame

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
    def draw(self, WIN):
        pygame.draw.rect(WIN, self.currentColor, self.rect, 0, 10)
        pygame.draw.rect(WIN, (255, 255, 255), self.rect, 2, 10)
        self.drawText(WIN)

    # draws the buttons text
    def drawText(self, WIN):
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