# imports
import pygame
import createProblem as eq
import threading
# screens
from GameLoop import GameLoop
from LoseScreen import LoseScreen
from LoadingScreen import LoadingScreen
from MainMenu import MainMenu
from LevelScreen import LevelScreen

# initialize pygame
pygame.init()

# initialize the window
WIN = pygame.display.set_mode((0, 0))
WIDTH, HEIGHT = WIN.get_width(), WIN.get_height()
FPS = 120 # 60 - 144

# set the basic font
font = pygame.font.Font(None, 100)

# load and play music / load sound fx's
pygame.mixer.music.load('assets/game_music/Pixelated Horizons.mp3')
pygame.mixer.music.play(-1)
CorrectSound = pygame.mixer.Sound('assets/game_music/correct.mp3')

# variable to the save the current screen / Mode
currentMode = "main-menu"
currentLevel = 1

# called everytime a screen is changed to check what is the next screen
def RunGame():
    global currentMode
    while currentMode != "quit":
        if currentMode == "gameloop":
            currentMode = GameLoop(WIDTH, HEIGHT, WIN, FPS, CorrectSound, currentLevel)
        if currentMode == "levelscreen":
            currentMode, currentLevel = LevelScreen(WIDTH, HEIGHT, WIN, FPS)
        elif currentMode == "loadingScreen":
            thread = threading.Thread(target=eq.getEquations, args=(100,))
            currentMode = LoadingScreen(thread, WIDTH, HEIGHT, WIN)
        elif currentMode == "main-menu":
            currentMode = MainMenu(WIDTH, HEIGHT, WIN, FPS)
        elif currentMode == "lose-screen":
            currentMode = LoseScreen(WIDTH, HEIGHT, WIN, FPS)

# start the game if I play this current file
if __name__ == "__main__":
    RunGame()

# exit pygame if all windows closed
pygame.quit()
