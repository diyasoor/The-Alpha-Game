import pygame
import image
from settings import *
from glove_tracking import GloveTracking
import cv2

class Glove:
    def __init__(self):
        self.orig_image = image.load("assets/images/ironman.png", size=(GLOVE_SIZE, GLOVE_SIZE))
        self.image = self.orig_image.copy()
        self.image_smaller = image.load("assets/images/ironman.png", size=(GLOVE_SIZE - 50, GLOVE_SIZE - 50))
        self.rect = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, GLOVE_HITBOX_SIZE[0], GLOVE_HITBOX_SIZE[1])
        self.left_click = False

    # change the glove pos center at the mouse pos
    def follow_mouse(self):
        self.rect.center = pygame.mouse.get_pos()

    def follow_mediapipe_glove(self, x, y):
        self.rect.center = (x, y)

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (200, 60, 0), self.rect)

    def draw(self, surface):
        image.draw(surface, self.image, self.rect.center, pos_mode="center")

        if DRAW_HITBOX:
            self.draw_hitbox(surface)

    # return a list with all targets that collide with the glove hitbox
    def on_target(self, targets):
        return [target for target in targets if self.rect.colliderect(target.rect)]

    # will kill the targets that collide with the glove when the left mouse button is pressed
    def kill_targets(self, targets, score, sounds):
        if self.left_click: # if left click
            for target in self.on_target(targets):
                target_score = target.kill(targets)
                score += target_score
                sounds["slap"].play()
                if target_score < 0:
                    sounds["screaming"].play()
        else:
            self.left_click = False
        return score
