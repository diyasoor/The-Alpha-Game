import pygame

WINDOW_NAME = "THE ALPHA GAME"
GAME_TITLE = WINDOW_NAME

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700

FPS = 90
DRAW_FPS = True

# sizes
BUTTONS_SIZES = (250, 90)
GLOVE_SIZE = 200
GLOVE_HITBOX_SIZE = (60, 80)
THANOS_SIZES = (100, 80)
THANOS_SIZE_RANDOMIZE = (1,2) # for each new thanos, it will multiply the size with a random value between X and Y
CAPTAIN_SIZES = (80, 100)
CAPTAIN_SIZE_RANDOMIZE = (1.2, 1.5)

# drawing - it will draw all the hitbox
DRAW_HITBOX = False

# animation -> The frame of the target will change every X sec
ANIMATION_SPEED = 0.08

# difficulty
GAME_DURATION = 60 # the game will last X sec
THANOS_SPAWN_TIME = 1
THANOS_MOVE_SPEED = {"min": 1, "max": 5}
CAPTAIN_PENALTY = 1 # will remove X of the score the player (if he kills captain)

# colors -> second is the color when the mouse is on the button
COLORS = {"title": (89, 0, 54), "score": (42, 12, 36), "timer": (42, 12, 36),
          "high_score": (255, 255, 255),"buttons": {"default": (56, 67, 209),
          "second": (87, 99, 255), "text": (255, 255, 255), "shadow": (46, 54, 163)}}

#second: 23, 176, 190
#shadow: 3, 90, 107
#default: 3, 133, 155

# sounds
MUSIC_VOLUME = 0.2  #value between 0 and 1
SOUNDS_VOLUME = 1

# fonts
pygame.font.init()
FONTS = {}
FONTS["small"] = pygame.font.Font("assets/PixelGameFont.ttf", 20)
FONTS["medium"] = pygame.font.Font("assets/PixelGameFont.ttf", 50)
FONTS["big"] = pygame.font.Font("assets/PixelGameFont.ttf", 90)