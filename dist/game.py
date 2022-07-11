import pygame
import time
import random
from settings import *
from background import Background
from glove import Glove
from glove_tracking import GloveTracking
from thanos import Thanos
from captain import Captain
import cv2
import ui

high_score = 0
screen = pygame.display.set_mode((1000, 700))
game_over_surface = pygame.image.load("assets/images/game_over.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(495,350))


class Game:
    high_score = 0
    def __init__(self, surface):
        self.surface = surface
        self.background = Background()

        # Load camera
        self.cap = cv2.VideoCapture(0)

        self.sounds = {}
        self.sounds["slap"] = pygame.mixer.Sound(f"assets/Sounds/slap.wav")
        self.sounds["slap"].set_volume(SOUNDS_VOLUME)
        self.sounds["screaming"] = pygame.mixer.Sound(f"assets/Sounds/screaming.wav")
        self.sounds["screaming"].set_volume(SOUNDS_VOLUME)


    def reset(self): # reset all the needed variables
        self.glove_tracking = GloveTracking()
        self.glove = Glove()
        self.targets = []
        self.targets_spawn_timer = 0
        self.score = 0
        self.game_start_time = time.time()


    def spawn_targets(self):
        t = time.time()
        if t > self.targets_spawn_timer:
            self.targets_spawn_timer = t + THANOS_SPAWN_TIME

            # increase the probability that the target will be a bee over time
            nb = (GAME_DURATION-self.time_left)/GAME_DURATION * 100  / 2  # increase from 0 to 50 during all  the game (linear)
            if random.randint(0, 100) < nb:
                self.targets.append(Captain())
            else:
                self.targets.append(Thanos())

            # spawn a other mosquito after the half of the game
            if self.time_left < GAME_DURATION/2:
                self.targets.append(Thanos())

    def load_camera(self):
        _, self.frame = self.cap.read()


    def set_glove_position(self):
        self.frame = self.glove_tracking.scan_gloves(self.frame)
        (x, y) = self.glove_tracking.get_hand_center()
        self.glove.rect.center = (x, y)

    def draw(self):
        # draw the background
        self.background.draw(self.surface)
        # draw the targets
        for target in self.targets:
            target.draw(self.surface)
        # draw the glove
        self.glove.draw(self.surface)
        # draw the score
        ui.draw_text(self.surface, f"SCORE: {self.score}", (19, 5), COLORS["score"], font=FONTS["medium"],
                    shadow=True, shadow_color=(255,255,255))
        # draw the time left 160, 40, 0
        timer_text_color = (165, 31, 5) if self.time_left < 5 else COLORS["timer"] # change the text color if less than 5 s left
        ui.draw_text(self.surface, f"TIME LEFT: {self.time_left}", (570, 5),  timer_text_color, font=FONTS["medium"],
                    shadow=True, shadow_color=(255,255,255))


    def game_time_update(self):
        self.time_left = max(round(GAME_DURATION - (time.time() - self.game_start_time), 1), 0)



    def update(self):

        self.load_camera()
        self.set_glove_position()
        self.game_time_update()

        self.draw()

        if self.time_left > 0:
            self.spawn_targets()
            (x, y) = self.glove_tracking.get_hand_center()
            self.glove.rect.center = (x, y)
            self.glove.left_click = self.glove_tracking.glove_closed
            print("Hand closed", self.glove.left_click)
            if self.glove.left_click:
                self.glove.image = self.glove.image_smaller.copy()
            else:
                self.glove.image = self.glove.orig_image.copy()
            self.score = self.glove.kill_targets(self.targets, self.score, self.sounds)
            for target in self.targets:
                target.move()

        else: # when the game is over
            screen.blit(game_over_surface, game_over_rect)
            if(self.score > self.high_score):
                self.high_score = self.score

            ui.draw_text(self.surface, f"HIGH SCORE : {self.high_score}", (301, 100), COLORS["high_score"],
                         font=FONTS["medium"], shadow=True, shadow_color=(0, 0, 0))

            if ui.button(self.surface, 540, "RETRY", click_sound=self.sounds["slap"]):
                return "menu"


        cv2.imshow("FRAME", self.frame)
        cv2.waitKey(1)
