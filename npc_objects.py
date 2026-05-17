import pygame
import random
from settings import *


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        rockImages = ["rocks/rock1.png", "rocks/rock2.png", "rocks/rock3.png"]
        chosenRock = random.choice(rockImages)

        self.original_image = pygame.image.load(chosenRock).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (70, 70))
        self.image = self.original_image

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 40)
        self.rect.y = random.randint(-300, -50)

        self.speed = random.randint(5, 9)
        self.angle = 0
        self.rotation_speed = random.randint(-5, 5)

    def update(self):
        self.rect.y += self.speed
        self.angle += self.rotation_speed

        # I rotated the original image in this part to avoid distortion of the image.
        self.image = pygame.transform.rotate(self.original_image, self.angle)

        if self.rect.top > HEIGHT:
            self.rect.y = random.randint(-300, -50)
            self.rect.x = random.randint(0, WIDTH - 40)