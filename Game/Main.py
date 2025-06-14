# imports
import Levels
import pygame
import createProblem as eq
import threading
# screens
from GameLoop import GameLoop
from LoseScreen import LoseScreen
from LoadingScreen import LoadingScreen
from MainMenu import MainMenu
from LevelScreen import LevelScreen
from Levels import makeLevels
from SkinScreen import SkinScreen

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
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
CorrectSound = pygame.mixer.Sound('assets/game_music/correct.mp3')
CorrectSound.set_volume(0.7)
WrongSound = pygame.mixer.Sound('assets/game_music/wrong.mp3')
WrongSound.set_volume(0.7)

# variable to the save the current screen / Mode
currentMode = "main-menu"

# init the levels
makeLevels(WIDTH)

# called everytime a screen is changed to check what is the next screen
def RunGame():
    global currentMode
    while currentMode != "quit":
        if currentMode == "gameloop":
            currentMode, Levels.currentLevel = GameLoop(WIDTH, HEIGHT, WIN, FPS, CorrectSound, WrongSound, Levels.currentLevel)
        elif currentMode == "levelscreen":
            currentMode, Levels.currentLevel = LevelScreen(WIDTH, HEIGHT, WIN, FPS)
        elif currentMode == "loadingScreen":
            thread = threading.Thread(target=eq.getEquations, args=(100,))
            currentMode = LoadingScreen(thread, WIDTH, HEIGHT, WIN)
        elif currentMode == "main-menu":
            currentMode = MainMenu(WIDTH, HEIGHT, WIN, FPS)
        elif currentMode == "lose-screen":
            currentMode = LoseScreen(WIDTH, HEIGHT, WIN, FPS)
        elif currentMode == "skinscreen":
            currentMode = SkinScreen(WIDTH, HEIGHT, WIN)

# start the game if I play this current file
if __name__ == "__main__":
    RunGame()

# exit pygame if all windows closed
pygame.quit()
