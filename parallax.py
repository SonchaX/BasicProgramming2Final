import pygame
from settings import *


class ParallaxLayer:
    def __init__(self, filename, speed):
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.speed = speed
        self.x1 = 0
        self.x2 = WIDTH

    def update(self, moveDir):
        self.x1 -= self.speed * moveDir
        self.x2 -= self.speed * moveDir

        # If the first background leaves, it goes behind the other background for the loop.
        if self.x1 <= -WIDTH:
            self.x1 = self.x2 + WIDTH
        if self.x2 <= -WIDTH:
            self.x2 = self.x1 + WIDTH

        if self.x1 >= WIDTH:
            self.x1 = self.x2 - WIDTH
        if self.x2 >= WIDTH:
            self.x2 = self.x1 - WIDTH

    def draw(self, screen):
        screen.blit(self.image, (self.x1, 0))
        screen.blit(self.image, (self.x2, 0))


class ParallaxBg:
    def __init__(self, level):
        self.layers = []

        if level == 1:
            layerCount = 7
            layerSpeeds = [0.5, 1.0, 1.5, 2.0, 2.5, 3.5, 5.0]
        elif level == 2:
            layerCount = 7
            layerSpeeds = [0.5, 1.0, 1.5, 2.0, 2.5, 3.5, 5.0]
        elif level == 3:
            layerCount = 9
            layerSpeeds = [0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.5, 5.0]
        elif level == 4:
            layerCount = 7
            layerSpeeds = [0.5, 1.0, 1.5, 2.0, 2.5, 3.5, 5.0]
        else:
            layerCount = 7
            layerSpeeds = [0.5, 1.0, 1.5, 2.0, 2.5, 3.5, 5.0]

        for i in range(layerCount):
            filename = f"background/level{level}_bg{i+1}.png"
            self.layers.append(ParallaxLayer(filename, layerSpeeds[i]))

    def update(self, game_state, moveDir):
        if game_state == "PLAYING":
            for layer in self.layers:
                layer.update(moveDir)

    def draw(self, screen):
        for layer in self.layers:
            layer.draw(screen)