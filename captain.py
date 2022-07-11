import pygame
import random
import image
from settings import *
from thanos import Thanos


class Captain(Thanos):
    def __init__(self):
        # size
        random_size_value = random.uniform(CAPTAIN_SIZE_RANDOMIZE[0], CAPTAIN_SIZE_RANDOMIZE[1])
        size = (int(CAPTAIN_SIZES[0] * random_size_value), int(CAPTAIN_SIZES[1] * random_size_value))
        # moving
        moving_direction, start_pos = self.define_spawn_pos(size)
        # sprite
        self.rect = pygame.Rect(start_pos[0], start_pos[1], size[0] // 1.4, size[1] // 1.4)
        self.images = [image.load("assets/images/captain.png", size=size, flip=moving_direction == "right")]# load the images
        self.current_frame = 0
        self.animation_timer = 0

    def kill(self, thanos):  # remove the mosquito from the list
        thanos.remove(self)
        return -CAPTAIN_PENALTY
