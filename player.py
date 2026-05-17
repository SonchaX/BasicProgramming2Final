import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.run_frames = []
        self.idle_frames = []

        for i in range(10):
            img = pygame.image.load(f"player/run{i+1}.png").convert_alpha()
            img = pygame.transform.scale(img, (100, 100))
            self.run_frames.append(img)

        idleImg = pygame.image.load("player/idle.png").convert_alpha()
        idleImg = pygame.transform.scale(idleImg, (100, 100))
        self.idle_frames.append(idleImg)

        self.frame_index = 0
        self.animation_timer = 0

        self.facing_right = True
        self.state = "idle"
        self.is_moving = False
        self.move_dir = 0

        self.invincible = False
        self.invincibility_timer = 0

        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 180)

        self.hp = 3
        self.distance = 0
        self.speed = 6

    def update(self):
        keys = pygame.key.get_pressed()
        self.is_moving = False
        self.move_dir = 0

        if keys[pygame.K_LEFT]:
            self.is_moving = True
            self.facing_right = False
            self.move_dir = -1

        if keys[pygame.K_RIGHT]:
            self.is_moving = True
            self.facing_right = True
            self.move_dir = 1

        if self.is_moving:
            if self.state != "run":
                self.state = "run"
                self.frame_index = 0
        else:
            if self.state != "idle":
                self.state = "idle"
                self.frame_index = 0

        self.animation_timer += 1
        
        # I changed the animation frame every 4 clicks so it doesn't look too fast.
        if self.state == "run":
            if self.animation_timer % 4 == 0:
                self.frame_index += 1
                if self.frame_index >= len(self.run_frames):
                    self.frame_index = 0
            self.image = self.run_frames[self.frame_index]
        else:
            if self.animation_timer % 6 == 0:
                self.frame_index += 1
                if self.frame_index >= len(self.idle_frames):
                    self.frame_index = 0
            self.image = self.idle_frames[self.frame_index]

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.invincible:
            self.invincibility_timer -= 1
            if self.invincibility_timer <= 0:
                self.invincible = False