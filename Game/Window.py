import pygame

# a class to make an easy window with a text
class Window:
    def __init__(self, text, x, y, size):
        self.text = text
        self.show = False
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, size)

    # draw the window if show is True
    def draw(self, WIN):
        if self.show:
            pygame.draw.rect(WIN, (255, 128, 0), (self.x, self.y, 500, 800), 0, 20)
            pygame.draw.rect(WIN, (255, 255, 255), (self.x, self.y, 500, 800), 2, 20)
            for y, txt in enumerate(self.text):
                text_s = self.font.render(txt, 1, (0, 0, 0))
                WIN.blit(text_s, (self.x+20, 200+y*40))
                